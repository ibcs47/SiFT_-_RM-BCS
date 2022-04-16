from ctypes import FormatError
import socket
from dataclasses import asdict
import shutil
import os

IP = socket.gethostbyname(socket.gethostname())

PORT = 5150

ADDR = (IP, PORT)

FORMAT = "utf-8"

SIZE = 1024

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def command_handler(cmd):

    cmd=cmd.split(maxsplit=1)
    
    if cmd[0] == "pwd":
        __pwd__()
        
    elif cmd[0] == "lst":
        __lst__()
    elif cmd[0]== "chd":
        __chd__(cmd[1])
        
    elif cmd[0]== "mkd":
        __mkd__(cmd[1])
        
    elif cmd[0]== "del":
        __del__(cmd[1])

    elif cmd[0]== "upl":
        __upl__(cmd[1])
        
    else:
        print("Invalid command!")

def __pwd__():
    path=os.getcwd()
    print(path)

def __lst__():
    path=os.getcwd()
    print(os.listdir(path))
    
def __chd__(arg):
    try:
        os.chdir(arg)
        print("Working directory changed to: {0}".format(os.getcwd()))
    except FileNotFoundError:
        print("Directory: {0} does not exist".format(arg))
    except NotADirectoryError:
        print("{0} is not a directory".format(arg))
    except PermissionError:
        print("You do not have permissions to change to {0}".format(arg))
        
def __mkd__(arg):
    os.mkdir(arg)

def __del__(arg):
    try:
        os.remove(arg)
        print("Deleted file: {0}".format(arg))
    except FileNotFoundError:
        print("File/Directory: {0} does not exist".format(arg))
    except IsADirectoryError:
        try:
            shutil.rmtree(arg)
            print("Delete directory: {0}".format(arg))
        except OSError:
            print("File/Directory: {0} does not exist".format(arg))
    except PermissionError:
        print("You do not have permissions to change to {0}".format(arg))

def __upl__(arg):
    try:
        file = open(arg,"r")
        data = file.read()
        client.send(arg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("SERVER: {0}".format(msg))
        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("SERVER: {0}".format(msg))
        file.close()

    except OSError:
        print("File: {0} does not exist".format(arg))

def __dnl__(arg):
    try:
        client.send(arg.encode(FORMAT))
        with open(os.path.join(os.getcwd(), arg), 'wb') as file_to_write:
            while True:
                data = socket.recv(SIZE)
                if not data:
                    break
                file_to_write.write(data)
            file_to_write.close()

    except OSError:
        print("File: {0} does not exist".format(arg))
    
command=""

while(command != "exit"):
    
    command=input("Enter a command: ")
    command_handler(command)
