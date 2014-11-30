from enum import Enum


class ResponseType(Enum):
    Say = 1
    Do = 2
    Notice = 3
    Raw = 4


class IRCResponse(object):
    def __init__(self, messageType, response, target):
        self.Type = messageType
        try:
            self.Response = unicode(response, 'utf-8')
        except TypeError:  # Already utf-8?
            self.Response = response
        self.Target = target
