
__cfg_set = False
__config = {
    "scale": 5
}

def set_cfg(config: dict):
    """
    only can be called once,
    make sure to call before creating objects
    """
    global __cfg_set, __config

    if __cfg_set:
        raise TypeError("config already set")

    __cfg_set = True
    __config = config.copy()

def get_cfg(key: str):
    return __config[key]
