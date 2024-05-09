
__cfg_set = False
__config = {
    "scale": 5,
    "dialogue_width": 650,
    "dialogue_height": 200,
    "dialogue_border_width": 2,
    "dialogue_padding": 40,
    "dialogue_bg_color": (0, 0, 0),
    "dialogue_border_color": (255, 255, 255),
    "panel_border_width": 2,
    "panel_padding": 5,
    "panel_bg_color": (0, 0, 0, 200),
    "panel_border_color": (255, 255, 255, 200)
}

def set_cfg(config: dict):
    """only can be called once,
    make sure to call before creating objects"""
    global __cfg_set, __config

    if __cfg_set:
        raise TypeError("config already set")

    __cfg_set = True
    __config = config.copy()

def append_cfg(config: dict):
    """appends keys & values to the config"""
    global __config
    __config.update(config)

def get_cfg(key: str):
    return __config[key]
