from django.core.cache import cache
from random import randint
TiME = 100

def generate_otp():
    return str(randint(100000 , 999999))


def cashe_otp(email : str):
    otp = generate_otp()
    cache.set(f"otp_{email}" , otp , timeout=TiME)
    return otp

def verify_otp(email : str , otp : str):
    saved = cache.get(f"otp_{email}")
    return saved == otp