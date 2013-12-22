import platform
import subprocess
import sys
from subprocess import PIPE

__author__ = 'Kosan'


class Launcher():
    def __init__(self):
        self.server = subprocess.Popen(args=[],
                                       executable=Helpers.get_bin_path(),
                                       stdin=PIPE,
                                       stdout=PIPE,
                                       stderr=PIPE)

    def start(self):
        while self.server.poll() is None:
            inline = self.server.stdout.readline().decode("utf-8")
            if not inline:
                break
            elif Parser.parseline(inline) is not None:
                print(Parser.parseline(inline))

    def main(self):
        pass


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
                    print(Server.get_active_players())
                if line.endswith(" connected"):
                    player = line[14:line.rfind("'", 14)]
                    uid = line[line.rfind("<") + 1:line.rfind(">")]
                    ip = line[line.rfind("(") + 1:line.rfind(":")]
                    Server.player_login(player, uid, ip)
                    print(Server.get_active_players())


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
        return self.players


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


try:
    Server = Server()
    test = Launcher()
    test.start()
finally:
    test.server.terminate()
