def logger_check_func(func):

    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as p:
            print(f'Ошибка: {p}')
            raise p

    return wrapped