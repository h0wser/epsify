#!/bin/python

# TODO: sanitize input some way (client)
# lock down server
# python 3

import socket
import os
from parser import Parser
from parser import MessageTypeError
from parser import ChannelError
from parser import MessageType

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "epsilon.systems"
channel = "#radio"
port = 6667
nick = "listener"

uri = 'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:'

p = Parser(channel)

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


def connect(server, port):
    sock.connect((server, port))
    sock.send(bytes("USER " + nick + " " + nick + " " + nick + " " + nick + "\n", "UTF-8"))
    sock.send(bytes("NICK " + nick + "\n", "UTF-8"))

# no error checking atm to ensure it's a real spotify uri but whatevva
def play_song(song):
    cmd = uri + song
    os.system(cmd)

def exit():
    sock.close()

#lol
def pingpong(data):
    print('Replying to ' + data)
    newdata = list(data)
    newdata[1] = 'O'
    sock.send(bytes("".join(newdata) + '\n', "UTF-8"))


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
    if (msg.find("PING") > -1):
        pingpong(msg)
    else:

        try:
            parsed_msg = p.parse_msg(msg)
            #print('PARSED_MSG: ' + parsed_msg.sender + ':' + parsed_msg.msg_type + ':' + parsed_msg.data)
            if parsed_msg.msg_type == MessageType.SONG_PLAY:
                play_song(parsed_msg.data)
        except MessageTypeError:
            print('Unknown message type')
        except ChannelError:
            print('Not listening on channel')
        except Exception:
            print('Something else broke')
