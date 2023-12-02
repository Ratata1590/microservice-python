from multiprocessing.pool import ThreadPool
from xml.etree.ElementInclude import default_loader
from persistqueue import SQLiteAckQueue
from persistqueue.exceptions import Empty
import traceback
import importlib.util
import sys
import argparse
import os


def calculate(item):
    global target_module
    try:
        data = item["data"]
        target_module.process(data)
        del data["retry"]
        data["error"] = None
        input_queue.ack(item)
    except:
        data["error"] = traceback.format_exc()
        data["retry"] -= 1
        input_queue.update(item)
        if data["retry"] == 0:
            input_queue.ack(item)
            del data["retry"]
            error_queue.put(data)
        else:
            input_queue.nack(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="execute node")
    parser.add_argument(
        "--filepath",
        type=str,
        default=os.environ.get("FILEPATH") or "node.py",
        help="path to node .py file",
    )
    parser.add_argument(
        "--poolsize",
        type=int,
        default=os.environ.get("POOLSIZE") or 1,
        help="worker poolsize default=1",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=os.environ.get("RETRY") or 1,
        help="retry policy default=1",
    )

    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("module.name", args.filepath)
    target_module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = target_module
    spec.loader.exec_module(target_module)
    target_module.init()

    input_queue = SQLiteAckQueue(
        path=os.path.join("queues", args.filepath),
        name="input",
        multithreading=True,
        auto_commit=True,
    )
    error_queue = SQLiteAckQueue(
        path=os.path.join("queues", args.filepath),
        name="error",
        multithreading=True,
        auto_commit=True,
    )
    current_id = None
    with ThreadPool(args.poolsize) as pool:
        while True:
            try:
                if current_id is None:
                    item = input_queue.get(timeout=1, raw=True)
                else:
                    item = input_queue.get(
                        timeout=1, id=current_id, next_in_order=True, raw=True
                    )
                current_id = item["pqid"]
                if "retry" not in item["data"]:
                    item["data"]["retry"] = args.retry
                pool.apply_async(calculate, (item,))
            except Empty:
                pass
            finally:
                input_queue.clear_acked_data(keep_latest=0)
