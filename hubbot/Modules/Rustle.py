from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
import random
import string


class Rustle(ModuleInterface):
    triggers = ["rustle"]
    help = "rustle <rustlee> - There's no need to be upset."

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) < 1:
            return IRCResponse(ResponseType.Say, "Rustle who?", message.ReplyTo)
        else:
            roll = random.randint(1, 20)
            if roll == 1:
                return IRCResponse(ResponseType.Say, "{} has rustled their own jimmies in their critical failure!".format(message.User.Name), message.ReplyTo)
            elif (roll > 1) and (roll < 12):
                return IRCResponse(ResponseType.Say, "{}'s jimmies status: unrustled".format(string.join(message.ParameterList)), message.ReplyTo)
            elif (roll > 11) and (roll < 20):
                return IRCResponse(ResponseType.Say, "{}'s jimmies status: rustled".format(string.join(message.ParameterList)), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "{}'s jimmies status: CRITICAL RUSTLE".format(string.join(message.ParameterList)), message.ReplyTo)
