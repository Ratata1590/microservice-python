from persistqueue import SQLiteAckQueue
import sys


if __name__ == "__main__":
    error_q = SQLiteAckQueue(path=sys.argv[1], name="error", multithreading=True)
    while True:
        item = error_q.get(raw=True, timeout=1)
        print(item)
