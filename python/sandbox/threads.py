from threading import Thread
import time
import sys

def loop_function():
    j=0
    while True:
        print(f"Loop {j}")
        time.sleep(0.2)
        if j >= 100:
            sys.exit()
        j += 1

def main():
    thread = Thread(target=loop_function)
    thread.start()

    # Do other tasks while the loop runs in the background
    for i in range(5):
        print(f"Main thread doing other tasks, iteration {i}")
        time.sleep(2)
    sys.exit()

if __name__ == "__main__":
    main()