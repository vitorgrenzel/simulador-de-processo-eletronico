"""Utilies to User app"""
import base64
import random


def convert_datatime_to_base64(datetime):
    """Receive datetime and return string base64"""
    encoded = base64.urlsafe_b64encode("%d".encode() % int(datetime.strftime("%Y%m%d%H%M%S")))
    return str(encoded.decode())

def generate_random_key():
    return str('%32x' % random.getrandbits(16*8))
