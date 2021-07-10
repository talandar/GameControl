

MODULE_KEY = "MODULE"
ARGS_KEY = "ARGS"


def generate_message(module, args):
    message = {}
    message[MODULE_KEY] = module
    message[ARGS_KEY] = args
    return message


def split_message(message):
    return message[MODULE_KEY], message[ARGS_KEY]


def message_module(message):
    return message[MODULE_KEY]


def message_args(message):
    return message[ARGS_KEY]
