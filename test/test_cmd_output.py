#!/usr/bin/env python3
import unittest
import rndoutput
import subprocess
import os
import signal
import sys
import time
import select


class Process:
    def __init__(self, cmd_line):
        self.cmd_line = cmd_line

    def run(self):
        self.proc = subprocess.Popen(
            self.cmd_line,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
            shell=True,
        )

    def stop(self):
        if self.proc is not None:
            # Stop gets called from a seperate thread
            # so shutdown may already be in progress
            # when we try to kill - therefore ignore errors
            try:
                # kill - including all children of process
                self.killing = True
                os.killpg(self.proc.pid, signal.SIGKILL)
            except Exception as e:
                self.fail()

    def wait_for_first_line(self):
        for line in self.proc.stdout:
            return line


class TestCommmandFirstLineOutput(unittest.TestCase):
    def setUp(self):
        p = Process("rndoutput.py 1 3")
        # p.run()

    def test_fails_if_command_doesnt_exist(self):
        p = Process("nonexistentprogram")
        self.assertRaises(FileNotFoundError, p.run)

    def test_fails_if_command_exits_before_timeout(self):
        self.fail()

    def test_fails_if_command_fails(self):
        self.fail()

    def test_fails_if_command_takes_more_than_timout_to_respond(self):
        self.fail()

    def test_returns_the_correct_value(self):
        self.fail()

    def test_can_handle_spaces_before_initial(self):
        self.fail()

    def test_can_handle_spaces_after_initial(self):
        self.fail()


def test_poll():
    # invoke process
    process = subprocess.Popen(shlex.split(command), shell=False, stdout=process.PIPE)

    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()


def test_old_way():
    start = time.time()
    cmd = " ".join(sys.argv[1:])
    print(f"Starting: {cmd}")
    proc = subprocess.Popen(
        # "./rndoutput.py 1 5",
        #'omxplayer test.720p.h264.mkv',
        cmd,
        stdout=subprocess.PIPE,
        bufsize=1,
        shell=True,
        universal_newlines=True,
    ) 
    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    timeout = 2
    while proc.poll() is None:
        if timeout is not None:
            poll_result = poll_obj.poll(1000 * timeout)
            if not poll_result:
                raise Exception("Timed out waiting for input")
        #line = proc.stdout.readline().decode("utf-8")
        line = proc.stdout.readline()
        if not line:
            raise Exception("Process suddenly died")
        #line = line.strip()
        #if line.strip() != "":
            #return line
        print(f"{time.time() - start:.2f}", line.strip(), flush=True)


def test_popen():
    start = time.time()
    cmd = " ".join(sys.argv[1:])
    print(f"Starting: {cmd}")
    with subprocess.Popen(
        # "./rndoutput.py 1 5",
        #'omxplayer test.720p.h264.mkv',
        cmd,
        stdout=subprocess.PIPE,
        bufsize=1,
        shell=True,
        universal_newlines=True,
    ) as p:
        for line in p.stdout:
            print(f"{time.time() - start:.2f}", line.strip(), flush=True)


def main():
    p = Process("./rndoutput.py 1 9")
    p.run()
    print("waiting")
    print(p.wait_for_first_line())
    print("waited")


if __name__ == "__main__":
    print(f"Called with arguments: {sys.argv}")
    #test_popen()
    test_old_way()
