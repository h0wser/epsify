from enum import Enum
import re

class ChannelError(Exception):
    def __init__(self, channel):
        self._channel = channel

class MessageTypeError(Exception):
    def __init__(self, msg_type):
        self._msg_type = msg_type

class MessageType(Enum):
    ERROR  = 1
    REQUEST = 2
    SONG_PLAY = 3
    SYNC = 4
    STATUS = 5


class Message:
    def __init__(self, msg_type, data, sender):
        self.msg_type = msg_type
        self.data = data
        self.sender = sender


class Parser:
    def __init__(self, channel):
        self._channel = channel;

    def parse_msg(self, msg):
        m = re.search('\#[a-z]+', msg)
        channel = m.group(0)[:len(m.group(0))]
        if not (channel == self._channel):
            raise ChannelError(channel)

        m = re.search('\:\[.+\]', msg)
        msg_type = m.group(0)[2:len(m.group(0))-1]

        mt = MessageType.ERROR
        if (msg_type.lower() == 'request'):
            mt = MessageType.REQUEST
        elif (msg_type.lower() == 'song_play'):
            mt = MessageType.SONG_PLAY
        elif (msg_type.lower() == 'sync'):
            mt = MessageType.SYNC
        elif (msg_type.lower() == 'status'):
            mt = MessageType.STATUS

        if mt == MessageType.ERROR:
            raise MessageTypeError(msg_type.lower())

        m = re.search('\:.+\!', msg)
        sender = m.group(0)[1:len(m.group(0))-1]

        m = re.search('\].*', msg)
        data = ''
        if not m == None:
            data = m.group(0)[2:]

        return Message(mt, data, sender)
