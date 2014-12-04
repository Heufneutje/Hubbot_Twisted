import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.message import IRCMessage


class Alias(ModuleInterface):
    triggers = ["alias", "unalias"]
    help = 'alias <alias> <command> <params> - aliases <alias> to the specified command and parameters\n' \
           'you can specify where parameters given to the alias should be inserted with $1, $2, $n. ' \
           'you can use $1+, $2+ for all parameters after the first, second one, etc. ' \
           'The whole parameter string is $0. $sender and $channel can also be used.'
    aliases = {}

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.bot.moduleHandler.mappedTriggers:
            return True
        return False

    def onLoad(self):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM aliases"):
                self.aliases[row[0]] = row[1].split(" ")
        for alias in self.aliases:
            self.bot.moduleHandler.mappedTriggers[alias] = self

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.triggers:
            if message.Command == "alias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may create new aliases!", message.ReplyTo)

                if len(message.ParameterList) <= 1:
                    return IRCResponse(ResponseType.Say, "Alias what?", message.ReplyTo)

                if message.ParameterList[0] in self.bot.moduleHandler.mappedTriggers:
                    return IRCResponse(ResponseType.Say, "'{}' is already a command!".format(message.ParameterList[0]), message.ReplyTo)

                if message.ParameterList[1] not in self.bot.moduleHandler.mappedTriggers and message.ParameterList[1] not in self.aliases:
                    return IRCResponse(ResponseType.Say, "'{}' is not a valid command or alias!".format(message.ParameterList[1]), message.ReplyTo)
                if message.ParameterList[0] in self.aliases.keys():
                    return IRCResponse(ResponseType.Say, "'{}' is already an alias!".format(message.ParameterList[0]), message.ReplyTo)

                aliasParams = []
                for word in message.ParameterList[1:]:
                    aliasParams.append(word)
                self._newAlias(message.ParameterList[0], aliasParams)

                return IRCResponse(ResponseType.Say, "Created a new alias '{}' for '{}'.".format(message.ParameterList[0], " ".join(message.ParameterList[1:])), message.ReplyTo)
            elif message.Command == "unalias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may remove aliases!", message.ReplyTo)

                if len(message.ParameterList) == 0:
                    return IRCResponse(ResponseType.Say, "Unalias what?", message.ReplyTo)

                if message.ParameterList[0] in self.aliases.keys():
                    self._deleteAlias(message.ParameterList[0])
                    return IRCResponse(ResponseType.Say, "Deleted alias '{}'".format(message.ParameterList[0]), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "I don't have an alias '{}'".format(message.ParameterList[0]), message.ReplyTo)

        elif message.Command in self.aliases.keys():
            newMessage = self._aliasedMessage(message)
            newCommand = newMessage.Command
            if newCommand in self.bot.moduleHandler.mappedTriggers:
                return self.bot.moduleHandler.mappedTriggers[newCommand].onTrigger(newMessage)
            elif newCommand in self.aliases:
                newMessage = self._aliasedMessage(message)
                return self.onTrigger(newMessage)

    def _newAlias(self, alias, command):
        self.aliases[alias] = command
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO aliases VALUES (?,?)", (alias, " ".join(command)))
            conn.commit()

    def _deleteAlias(self, alias):
        del self.aliases[alias]
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM aliases WHERE alias=?", (alias,))
            conn.commit()

    def _aliasedMessage(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.aliases.keys():
            alias = self.aliases[message.Command]
            newMsg = message.MessageString.replace(message.Command, " ".join(alias), 1)
            if "$sender" in newMsg:
                newMsg = newMsg.replace("$sender", message.User.Name)
            if "$channel" in newMsg and message.ChannelObj is not None:
                newMsg = newMsg.replace("$channel", message.ChannelObj.Name)

            if re.search(r'\$[0-9]+', newMsg):  # if the alias contains numbered param replacement points, replace them
                newMsg = newMsg.replace('$0',  u' '.join(message.ParameterList))
                for i, param in enumerate(message.ParameterList):
                    if newMsg.find(u"${}+".format(i+1)) != -1:
                        newMsg = newMsg.replace(u"${}+".format(i+1), u" ".join(message.ParameterList[i:]))
                    else:
                        newMsg = newMsg.replace(u"${}".format(i+1), param)
            else:  # if there are no numbered replacement points, append the full parameter list instead
                newMsg += u' {}'.format(u' '.join(message.ParameterList))
            return IRCMessage(message.Type, message.User.String, message.ChannelObj, newMsg, self.bot)
