__author__ = 'Kosan'


class Client(object):
    def __init__(self, sock):
        self.sock = sock

    def send(self, string):
        self.sock.send((string + "\r\n").encode())

    def connect(self):
        self.sock.connect(('irc.freenode.net', 6667))
        self.send("NICK Omnius")
        self.send("USER Omnius Omnius Omnius :Python IRC Client by Kosan Nicholas")
        try:
            with open('passwd') as f:
                self.send("PRIVMSG Nickserv :IDENTIFY " + f.read())
        except IOError:
            print("No passwd file found, cannot authenticate")

    def listen(self):
        while True:
            data = self.sock.recv(512).decode('utf-8').strip()
            #print(data)
            if len(data) == 0:
                print("Disconnected from IRC Network")
                self.sock.close()
                break
            if data == "EOF":
                print("End of File")
                self.sock.close()
                break
            if data.find("PING") != -1:
                self.send("PONG")