import socket
import threading
import landerdb
import json

class QuantumBroker:
    def __init__(self):
        self.sock = socket.socket()
        self.db = landerdb.Connect("nodes.db")
        self.port = 6554
        self.node_p = 5554
    def main(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            threading.Thread(target=self.handle, args=(obj,conn)).start()
    def handle(self, obj, conn):
        print conn
        self.db.insert("nodes", {conn[0]: self.node_p})
        with open("nodes.db", 'rb') as file:
            for x in file.readlines():
                obj.send(x)
        obj.close()
if __name__ == "__main__":
    QuantumBroker().main()
