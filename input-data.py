from persistqueue import SQLiteAckQueue
import os

if __name__ == "__main__":
    input_queue = SQLiteAckQueue(
        path=os.path.join("queues", "n2.py"),
        name="input",
        multithreading=True,
        auto_commit=True,
    )
    input_queue.clear_acked_data(keep_latest=0)
    for item in range(100):
        input_queue.put({"data": item, "error": None})
