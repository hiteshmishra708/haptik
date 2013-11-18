import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haptik_api.settings")

from api.lib.create_csv import *



#if __name__ == "__main__":
website_signup_csv()
beta_distrib_csv()
haptik_users()
user_favorites()
