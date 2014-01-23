import uuid 
from api.models.default import BetaDistrib

DISTRIB_URL = 'http://haptik.co/distribute/%s'


def my_random_string(string_length=8):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert uuid format to python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the uuid '-'.
    return random[0:string_length].lower() 


def create_beta_distrib_url(number):
    dis = BetaDistrib()
    dis.number = number
    dis.hex_code = my_random_string()
    dis.save()
    url = DISTRIB_URL % dis.hex_code
    return url


def find_distrib_by_hex(hex_code):
    dis = None
    try:
        dis = BetaDistrib.objects.get(hex_code = hex_code)
    except:
        pass
    return dis
