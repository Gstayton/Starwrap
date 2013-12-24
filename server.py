__author__ = 'Kosan'


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

    @staticmethod
    def parseline(line, server):
        line = line.strip()
        if "Info: " == line[0:6]:
            print(line)
            if "Client " == line[6:13]:
                if line.endswith(" disconnected"):
                    server.player_logout(line[14:line.rfind("'", 14)])
                if line.endswith(" connected"):
                    player = line[14:line.rfind("'", 14)]
                    uid = line[line.rfind("<") + 1:line.rfind(">")]
                    ip = line[line.rfind("(") + 1:line.rfind(":")]
                    server.player_login(player, uid, ip)

    @staticmethod
    def parse_stdout(process, server):
        while True:
            inline = process.stdout.readline().decode("utf-8")
            if inline is None:
                break
            else:
                Server.parseline(inline, server)