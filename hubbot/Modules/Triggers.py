from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Triggers(ModuleInterface):
    triggers = ["triggers"]
    help = "triggers [module] -- returns a list of all commands, if no module is specified, " \
           "returns all commands currently loaded."

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            if message.User.Name != message.ReplyTo:
                return IRCResponse(ResponseType.Say, "{} must be used over PM!".format(message.Command),
                                   message.ReplyTo)
            else:
                response = ", ".join(sorted(self.bot.moduleHandler.mappedTriggers.keys()))
                return IRCResponse(ResponseType.Say, response, message.ReplyTo)
        else:
            if message.ParameterList[0].lower() not in self.bot.moduleHandler.moduleCaseMapping:
                return IRCResponse(ResponseType.Say, "No module named \"{}\" is currently loaded!", message.ReplyTo)

            properName = self.bot.moduleHandler.moduleCaseMapping[message.ParameterList[0].lower()]
            module = self.bot.moduleHandler.modules[properName]

            return IRCResponse(ResponseType.Say,
                               "Module \"{}\" contains the triggers: {}".format(properName, ", ".join(module.triggers)),
                               message.ReplyTo)
