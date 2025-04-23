from database import create_tables
from models import add_user, get_users

add_user("zackone", "ikanbusuk@air.com", "ayam123")

users = get_users()
for user in users:
    print(user)
