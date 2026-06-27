
from slowapi import Limiter
from slowapi.util import get_remote_address

# Defining the limiter once
limiter = Limiter(key_func=get_remote_address)