import platform
import subprocess
import sys
from subprocess import PIPE
import threading
import cmd
#import irc

__author__ = 'Kosan'


class Launcher():
    def __init__(self):
        #self.irc_client = irc.Client()
        self.server = subprocess.Popen(args=[],
                                       executable=Helpers.get_bin_path(),
                                       stdin=PIPE,
                                       stdout=PIPE,
                                       stderr=PIPE)

    def start(self):
        #self.irc_client = irc.Client()
        #self.irc_client.connect()

        self.term = Terminal()
        self.parse = Helpers.parse_stdout
        # Thread for irc I/O
        #irc_thread = threading.Thread(target=self.irc_client.listen, name="IRC")
        # Thread for terminal input
        term_thread = threading.Thread(target=self.term.cmdloop, name="Terminal")
        # Thread for server process
        proc_thread = threading.Thread(target=self.parse, name="Server", args=(self.server,))
        proc_thread.start()
        term_thread.start()
        #irc_thread.start()
        while self.server.poll() is None:
            pass


class Terminal(cmd.Cmd):
    prompt = ""
    cmdqueue = False
    completekey = None
    file = None

    def __init__(self):
        cmd.Cmd.__init__(self)

    def do_players(self, arg):
        print("\n".join(Server.get_active_players()))

    def do_shutdown(self, arg):
        print("Stopping server")
        Launcher.server.terminate()
        sys.exit()


class Parser():
    def __init__(self):
        pass

    @staticmethod
    def parseline(line):
        line = line.strip()
        if "Info: " == line[0:6]:
            print(line)
            if "Client " == line[6:13]:
                if line.endswith(" disconnected"):
                    Server.player_logout(line[14:line.rfind("'", 14)])
                if line.endswith(" connected"):
                    player = line[14:line.rfind("'", 14)]
                    uid = line[line.rfind("<") + 1:line.rfind(">")]
                    ip = line[line.rfind("(") + 1:line.rfind(":")]
                    Server.player_login(player, uid, ip)


class Server():
    def __init__(self):
        # {username: {"uid": uid, "ip": ip, "active":bool}}
        self.players = {}
        # {sector: {coords: [planet, ..]}}
        self.worlds = {}
        pass

    def player_login(self, player, uid, ip):
        if player not in self.players:
            self.players[player] = {}
        self.players[player]["uid"] = uid
        self.players[player]["ip"] = ip
        self.players[player]["active"] = True

    def player_logout(self, player):
        self.players[player]["active"] = False
        #for name, ident in self.players.iteritems():
        #    if ident == uid:
        #        self.players[name: {"uid": None, "active": False}]

    def world_load(self, sector, coords, planet):
        pass

    def world_unload(self, sector, coords, planet):
        pass

    def get_active_players(self):
        plist = []
        for player in self.players:
            if self.players[player]['active']:
                plist.append(player)
        return plist


class Helpers():
    @staticmethod
    def get_bin_path():
        is64bit = sys.maxsize > 2 ** 32
        dirs = {
            "linux64": "linux64/launch_starbound_server.sh",
            "linux32": "linux32/launch_starbound_server.sh",
            "windows": "win32\starbound_server.exe",
            "mac": "Starbound.app\Contents\MacOS"  # //fixme Needs MacOS testing, almost certainly doesn't work
        }
        if platform.system().lower() == "linux" and is64bit:
            return dirs["linux64"]
        elif platform.system().lower() == "linux" and not is64bit:
            return dirs["linux32"]

        return dirs[platform.system().lower()]

    @staticmethod
    def parse_stdout(process):
        while True:
            inline = process.stdout.readline().decode("utf-8")
            if not inline:
                break
            else:
                Parser.parseline(inline)

    @staticmethod
    def parse_irc(client):
        while True:
            client.recv()


if __name__ == "__main__":
    try:
        Server = Server()
        Launcher = Launcher()
        Launcher.start()
    finally:
        Launcher.server.terminate()
