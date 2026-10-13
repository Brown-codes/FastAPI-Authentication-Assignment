import sys

from database import SessionLocal
from models import User

db = SessionLocal()
user = db.get(User, sys.argv[1])
if user is None:
    print("No such user")
else:
    user.role = "admin"
    db.commit()
    print(f"{user.username} is now admin")
db.close()