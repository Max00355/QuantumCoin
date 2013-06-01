import socket
import threading
import landerdb
import checkin
import send
import get_diff
import check
import json
import random
import os
import uuid
import cmd

class QuantumCoin:
    
    def __init__(self):
        self.sock = socket.socket()
        self.cmds = {
                "checkin":checkin.checkin,
                "send":send.send,
                "get_diff":get_diff.get_diff,
                "check":check.check,                
                }
        self.broker = ("192.168.1.5", 6554)
        self.port = 5554 # Do not change this

    def main(self):
        if not os.path.exists("nodes.db"):
            self.db = landerdb.Connect("nodes.db")
            self.get_nodes()
            self.send_checkin()
        self.db = landerdb.Connect("nodes.db")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            threading.Thread(target=self.handle, args=(obj, conn)).start()

    def handle(self, obj, conn):
        data = obj.recv(1024)
        data = json.loads(data)
        print data
        if 'cmd' in data:
            if data['cmd'] in self.cmds:
                self.cmds[data['cmd']](data, obj, conn) 
    def send_checkin(self):
        nodes = self.db.find("nodes", "all")
        addr = landerdb.Connect("wallet.db")
        addr_ = addr.find("data", "all")[0]
        addr = ""
        for x in addr_:
            addr = x
        for x in nodes:
            s = socket.socket()
            ip = None
            port = None
            for y in x:
                ip = y
                port = 5554
                break
            try:
                s.settimeout(1)
                s.connect((ip, int(port)))
                s.send(json.dumps({"cmd":"checkin", "addr":addr}))
            except Exception, error:
                s.close()
                continue
            s.close()
                    
    def get_nodes(self):
        sock = socket.socket()
        sock.connect(self.broker)
        with open("nodes.db", 'wb') as file:
            db = landerdb.Connect("wallet.db")
            addr = db.find("data", "all")[0]
            for x in addr:
                addr = x
                break
            data = {"addr":addr}
            sock.send(json.dumps(data))
            while True:
                get = sock.recv(1024)
                if get:
                    file.write(get)
                else:
                    break
        sock.close()
        print "Downloaded Nodes"


class Shell(cmd.Cmd):

    prompt = "QuantumShell$ "

    def do_transactions(self, line):
        db = landerdb.Connect("transactions.db")
        print db.find("transactions", "all")
    
    def do_send(self):
        pass

if __name__ == "__main__":
    if not os.path.exists("wallet.db"):
        db = landerdb.Connect("wallet.db")
        coins = landerdb.Connect("coins.db")
        transactions = landerdb.Connect("transactions.db")
        transactions.insert("transactions", {})
        db.insert("data", {uuid.uuid4().hex:uuid.uuid4().hex})
        coins.insert("coins", {})
    #threading.Thread(target=Shell().cmdloop).start()
    QuantumCoin().main()

