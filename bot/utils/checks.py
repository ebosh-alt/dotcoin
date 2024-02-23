def check_is_float(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False


