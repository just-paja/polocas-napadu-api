def check_auth(args, pred):
    _, info = args
    if not pred(info.context):
        raise Exception("Unauthorized")


def is_staff(func):
    def wrapper(*args, **kwargs):
        check_auth(args, lambda context: context.user.is_staff)
        return func(*args, **kwargs)

    return wrapper
