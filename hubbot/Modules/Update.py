from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import re
import subprocess


class Update(ModuleInterface):
    triggers = ["update"]
    help = "update - pulls the latest code from GitHub"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        subprocess.call(["git", "fetch"])

        output = subprocess.check_output(["git", "whatchanged", "..origin/master"])
        changes = re.findall('\n\n\s{4}(.+?)\n\n', output)

        if len(changes) == 0:
            return IRCResponse(ResponseType.Say, "The bot is already up to date.", message.ReplyTo)

        changes = list(reversed(changes))
        response = "New Commits: {}".format(" | ".join(changes))

        subprocess.call(["git", "pull"])

        return IRCResponse(ResponseType.Say, response, message.ReplyTo)
