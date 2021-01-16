import socket
import shlex
from threading import Thread
import json

# Mutli thread for concurrency
class ClientConcurrency(Thread):

    def __init__(self, conn, add):
        self.conn = conn
        self.add = add
        Thread.__init__(self)
        print("New thread started for client Address: ", self.add)
    
    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if not data: return
                data = data.decode("utf-8")
                s = shlex.split(data)
                if s[0] == "set" and len(s) >= 2:
                    dic[s[1]] = s[2]
                    write_data()
                    self.conn.send(bytes("The value is set successfully against the key: " + s[1], "utf-8"))
                elif s[0] == "get" and len(s) >= 1:
                    if s[1] in dic:
                        self.conn.send(bytes(dic[s[1]], "utf-8"))
                    else:
                        self.conn.send(bytes("Not found", "utf-8"))
                elif s[0] == "delete":
                    dic.pop(s[1])
                    write_data()
                    self.conn.send(bytes("key is deleted", "utf-8"))
                elif s[0] == "exit":
                    self.conn.close()
                    print("Connection is closed for client Address: ", self.add)
                    return
                else:
                    self.conn.send(bytes("Unknown operation", "utf-8"))
                # self.conn.send(data)
            except Exception as e:
                self.conn.send(bytes("Error: " + str(e), "utf-8"))


def write_data():
    with open('abc.json', 'w') as fi:
        try:
            json.dump(dic, fi)
        except json.decoder.JSONDecodeError:
            pass


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (
    '', # host
    3750 # port
)
sock.bind(server_address)
sock.listen(1)
print("Listening on my socket")
thread = []
dic = {}

# Loads the json file

with open('abc.json', 'r') as fi:
    try:
        dic = json.load(fi)
        # print(dic)
    except json.decoder.JSONDecodeError:
        pass

while True:
    conn, add = sock.accept()
    print("Address: ", add)
    try:
        newClientThread = ClientConcurrency(conn, add)
        newClientThread.start()
    except Exception as e:
        print("Error: " + str(e))
# Closing the socket
sock.close()