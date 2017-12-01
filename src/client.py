#!/bin/python

# TODO: sanitize input some way (client)
# lock down server
# python 3

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "epsilon.systems"
channel = "#radio"
port = 6667
nick = "listener"

def joinchan(chan):
    sock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = sock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def sendmsg(msg, target):
    sock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))

def ircquit(msg):
    sock.send(bytes("QUIT " + msg + "\n", "UTF-8"))

def playsong(song):
    pass

def connect(server, port):
    sock.connect((server, port))
    sock.send(bytes("USER " + nick + " " + nick + " " + nick + " " + nick + "\n", "UTF-8"))
    sock.send(bytes("NICK " + nick + "\n", "UTF-8"))

def parseuri(msg):
    index = msg.rfind("SONG:")
    if (index == -1):
        return ""
    else:
        return msg.sub(index)

def exit():
    sock.close()

def pingpong(server):
    None


connect(server, port)
joinchan(channel)
sendmsg("im here", channel)

while True:
    msg = sock.recv(2048).decode("UTF-8")
    msg = msg.strip('\n\r')

    if msg == "": # quit if we don't receive data
        exit()
        break

    print(msg)

    if (msg.find("PRIVMSG ") > -1):
        print("found msg")
