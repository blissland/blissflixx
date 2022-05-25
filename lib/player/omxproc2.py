import os, time
from .processpipe import ExternalProcess, ProcessException

OMX_CMD = "omxplayer --timeout 6000 -I "
_START_TIMEOUT = 6000
_CMD_FIFO = "cmdfifo"


class OmxplayerProcess2(ExternalProcess):
    def __init__(self):
        ExternalProcess.__init__(self, True)

    def _get_cmd(self, args):
        cmd = OMX_CMD
        if "subtitles" in args:
            cmd = cmd + "--align center --subtitles '" + args["subtitles"] + "' "
            cmd += "'" + args["outfile"] + "'"
        return "tail -f " + _CMD_FIFO + " | " + cmd

    def name(self):
        return "omxplayer with keys"

    def start(self, args):
        if not os.path.exists(_CMD_FIFO):
            os.system("mkfifo " + _CMD_FIFO)
            self._send_key("z")
        ExternalProcess.start(self, args)

    def stop(self):
        if os.path.exists(_CMD_FIFO):
            try:
                os.remove(_CMD_FIFO)
            except Exception:
                pass
        ExternalProcess.stop(self)

    def _send_key(self, key):
        os.system("echo -n " + key + " >> " + _CMD_FIFO + " &")

    def control(self, action):
        key = None
        if action == "pause" or action == "resume":
            key = "p"
        elif action == "stop":
            key = "q"
        elif action == "subminus":
            key = "d"
        elif action == "subplus":
            key = "f"
        elif action == "plus600":
            key = "$'\x1b\x5b\x41'"
        elif action == "minus600":
            key = "$'\x1b\x5b\x42'"
        elif action == "plus30":
            key = "$'\x1b\x5b\x43'"
        elif action == "minus30":
            key = "$'\x1b\x5b\x44'"
        elif action == "volup":
            key = "="
        elif action == "voldown":
            key = "-"
        if key is not None:
            self._send_key(key)

    def _ready(self):
        self._send_key("z")
        while True:
            line = self._readline(_START_TIMEOUT)
            if line.startswith("have a nice day"):
                raise ProcessException("omxplayer failed to start")
            elif line.startswith("Vcodec id unknown:"):
                raise ProcessException("Unsupported video codec")
            elif "Metadata:" in line:
                break
            elif "Duration:" in line:
                break
