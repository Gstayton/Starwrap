import cmd
import sys

__author__ = 'Kosan'


class TerminalExtras(cmd.Cmd):
    prompt = ""
    cmdqueue = False
    completekey = None
    file = None

    def __init__(self, server):
        cmd.Cmd.__init__(self)
        self.server = server

    def do_players(self, arg):
        print("\n".join(self.server.get_active_players()))

    def do_shutdown(self, arg):
        print("Stopping server")
        self.server.terminate()
        sys.exit()