
__cfg_set = False
__config = {
    "scale": 5
}

def set_cfg(config: dict):
    """Only can be called once"""
    global __cfg_set, __config

    if __cfg_set:
        raise TypeError("config already set")

    __cfg_set = True
    __config = config.copy()

def get_cfg(key: str):
    return __config[key]
