from hubbot.channel import IRCChannel
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Join(ModuleInterface):
    triggers = ["join"]
    help = 'join <channel> - makes the bot join the specified channel(s)'

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) > 0:
            responses = []
            for param in message.ParameterList:
                channel = param
                if not channel.startswith('#'):
                    channel = '#' + channel
                responses.append(IRCResponse(ResponseType.Raw, 'JOIN {}'.format(channel), ''))
                self.bot.channels[channel] = IRCChannel(channel)
            return responses
        else:
            return IRCResponse(ResponseType.Say, "{}, you didn't say where I should join".format(message.User.Name), message.ReplyTo)
