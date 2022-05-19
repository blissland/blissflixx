#!/usr/bin/env python3
import random
import argparse
import time


def rndoutput(
    initial_silence=1,
    running_time=3,
    possible_lines=["a", "b", "c", "d"],
    possible_delays=[0.1, 0.3, 0.5, 1],
    last_line="bye",
    print_delays=True,
    flush=True
):
    """This script outputs random lines to the console.
    initial_silence :       Amount of time until the first line in seconds
    running_time :          Total time the program runs in seconds
    possible_lines :        Pool of lines to choose randomly
    possible_delays :       Possible delays between lines in seconds
    last_line :             The last line to print
    """
    start = time.time()
    time.sleep(initial_silence)
    max_possible_delays = max(possible_delays)
    keep_going = True
    while keep_going:
        remaining =  start + running_time - time.time()
        delay = random.choice(possible_delays)
        line = random.choice(possible_lines)
        if delay > remaining:
            delay = max(remaining, 0)
            keep_going = False
        if print_delays:
            print(f'{delay:.2f}', end=' ')
        if flush:
            print(line, flush=True)
        else:
            print(line)
        time.sleep(delay)
    print(last_line)
    if print_delays:
        print(f"Total: {time.time() - start:.2f}")


def main():
    # TODO: receive parameters
    parser = argparse.ArgumentParser(description="Output random lines to the console")
    parser.add_argument(
        "initial", type=float, help="The delay for the first line in seconds"
    )
    parser.add_argument("total", type=float, help="Exit after this time in seconds")
    parser.add_argument('-t', '--time', action='store_true', help='Print delays')
    parser.add_argument('-f', '--flush', action='store_true', help='Flush buffer after each line')
    args = parser.parse_args()
    rndoutput(args.initial, args.total, print_delays=args.time, flush=args.flush)


if __name__ == "__main__":
    main()
