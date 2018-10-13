import user_agents

_device_classes = {
    (1, 0, 0): 0,
    (0, 1, 0): 1,
    (0, 0, 1): 2,
}

DEVICE_CLASS_NAMES = [
    'mobile',
    'tablet',
    'pc',
    'other',
]


def get_device_class(ua_string):
    ua = user_agents.parse(ua_string)
    return _device_classes.get(
         (int(ua.is_mobile), int(ua.is_tablet), int(ua.is_pc)),
         3
    )
