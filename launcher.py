import platform
import subprocess
import sys
from subprocess import PIPE
import threading
import socket
import imp
import cmd

import irc
import server
import terminal


class Main():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_client = irc.Client(self.sock)
        self.server_proc = subprocess.Popen(args=[],
                                            executable=Helpers.get_bin_path(),
                                            stdin=PIPE,
                                            stdout=PIPE,
                                            stderr=PIPE)
        self.term = Terminal(self.server_proc)

    def start(self):
        #self.irc_client.connect()

        # Thread for irc I/O
        #irc_thread = threading.Thread(target=self.irc_client.listen, name="IRC")
        #irc_thread.daemon = True
        # Thread for terminal input
        term_thread = threading.Thread(target=self.term.cmdloop, name="Terminal")
        term_thread.daemon = True
        # Thread for server process
        proc_thread = threading.Thread(target=server.Server.parse_stdout, name="Server", args=(self.server_proc,
                                                                                               Server_instance))
        proc_thread.daemon = True
        proc_thread.start()
        term_thread.start()
        #irc_thread.start()
        while self.server_proc.poll() is None:
            pass

    def restart_thread(self, thread_name):
        return threading.enumerate()


class Parser():
    def __init__(self):
        pass

    @staticmethod
    def parseline(line):
        line = line.strip()
        if "Info: " == line[0:6]:
            #print(line)
            if "Client " == line[6:13]:
                if line.endswith(" disconnected"):
                    Server_instance.player_logout(line[14:line.rfind("'", 14)])
                if line.endswith(" connected"):
                    player = line[14:line.rfind("'", 14)]
                    uid = line[line.rfind("<") + 1:line.rfind(">")]
                    ip = line[line.rfind("(") + 1:line.rfind(":")]
                    Server_instance.player_login(player, uid, ip)


class Terminal(terminal.TerminalExtras):
    def __init__(self, server_proc):
        cmd.Cmd.__init__(self)
        self.server = server_proc

    def do_reload(self, arg):
        print(Launcher.restart_thread(None))
        try:
            imp.reload(globals()[arg])
        except KeyError:
            print("Module not found")


class Helpers():
    @staticmethod
    def get_bin_path():
        is64bit = sys.maxsize > 2 ** 32
        dirs = {
            "linux64": "linux64/launch_starbound_server.sh",
            "linux32": "linux32/launch_starbound_server.sh",
            "windows": "win32\starbound_server.exe",
            "mac": "Starbound.app/Contents/MacOS/starbound_server", # //fixme Needs MacOS testing, might work?
            "darwin": "Starbound.app/Contents/MacOS/starbound_server"
        }
        if platform.system().lower() == "linux" and is64bit:
            return dirs["linux64"]
        elif platform.system().lower() == "linux" and not is64bit:
            return dirs["linux32"]

        return dirs[platform.system().lower()]

if __name__ == "__main__":
    try:
        Server_instance = server.Server()
        Launcher = Main()
        Launcher.start()
    finally:
        Launcher.server_proc.terminate()
