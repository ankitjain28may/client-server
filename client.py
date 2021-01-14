import socket


server_address = (
    '', # host
    3750 # port
)

cli = socket.socket()
cli.connect(server_address)

message = input("Client> ")

while message != "exit":
    cli.send(bytes(message, 'utf-8'))
    data  = cli.recv(1024)
    data = data.decode("utf-8")
    print(data)
    message = input("Client> ")
cli.send(bytes('exit', 'utf-8'))
cli.close()


# set key value key value
# get key
# delete key

# set (key abc) (value xyz)