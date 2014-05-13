from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars
from ModuleHandler import LoadModule, UnloadModule


class Module(ModuleInterface):
    triggers = ['load', 'reload', 'unload']
    help = "load/reload <function>, unload <function> - handles loading/unloading/reloading of functions. Use 'all' with load/reload to reload all active functions"

    def execute(self, Hubbot, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins can use {0}".format(message.Command), message.ReplyTo)

        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "You didn't specify a function name! Usage: {0}".format(self.help), message.ReplyTo)

        if message.Command.lower() in ['load', 'reload']:
            successes, failures, exceptions = self.load(message.ParameterList)

        elif message.Command.lower() == "unload":
            successes, failures, exceptions = self.unload(message.ParameterList)

        responses = []
        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' {1}ed successfully".format(', '.join(successes), message.Command.lower()), message.ReplyTo))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' failed to {1}, or (they) do not exist".format(', '.join(failures), message.Command.lower()), message.ReplyTo))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' threw an exception (printed to console)".format(', '.join(exceptions)), message.ReplyTo))

        return responses

    def load(self, funcNames):

        funcNameCaseMap = {f.lower(): f for f in funcNames}

        successes = []
        failures = []
        exceptions = []

        if len(funcNames) == 1 and 'all' in funcNameCaseMap:
            for name, func in GlobalVars.modules.iteritems():
                if name == 'FuncLoader':
                    continue

                LoadModule(name)
                LoadModule(name)

            return ['all functions'], [], []

        for funcName in funcNameCaseMap.keys():

            if funcName == 'funcloader':
                failures.append("FuncLoader (I can't reload myself)")

            else:
                try:
                    success = LoadModule(funcName)
                    if success:
                        LoadModule(funcName)
                        successes.append(GlobalVars.moduleCaseMapping[funcName])
                    else:
                        failures.append(funcNameCaseMap[funcName])

                except Exception, x:
                    exceptions.append(funcNameCaseMap[funcName])
                    print x.args

        return successes, failures, exceptions

    def unload(self, funcNames):

        funcNameCaseMap = {f.lower(): f for f in funcNames}

        successes = []
        failures = []
        exceptions = []

        for funcName in funcNameCaseMap.keys():
            try:
                success = UnloadModule(funcName)
                if success:
                    successes.append(funcNameCaseMap[funcName])
                else:
                    failures.append(funcNameCaseMap[funcName])
            except Exception, x:
                exceptions.append(funcNameCaseMap[funcName])
                print x.args

        return successes, failures, exceptions