prefix = ""


def set_prefix(new_prefix):
    global prefix
    prefix = new_prefix


def detect_prefix(mode: str):
    if mode == "test":
        return "sb:t."
    elif mode == "prod":
        return "sb."
    else:
        return mode


def auto_set_prefix(mode: str):
    global prefix
    prefix = detect_prefix(mode)


def get_prefix():
    return prefix
