from functools import wraps

AWAITING_BOTS = []


def subscriber(cls):
    """
    Pub-sub behaviour for notifying robots after route creating
    :param cls:
    :return:
    """
    @wraps(cls)
    def wrapper(*args, **kwargs):
        bot = cls(*args, **kwargs)
        AWAITING_BOTS.append(bot)
        return bot

    return wrapper
