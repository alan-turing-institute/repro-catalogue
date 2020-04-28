
from datetime import datetime


def create_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")
