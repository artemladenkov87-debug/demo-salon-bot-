import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SALON_NAME = os.getenv("SALON_NAME", "Beauty Studio")

SERVICES = [
    {"name": "Стрижка",     "price": 1500, "duration": 60},
    {"name": "Окрашивание", "price": 3500, "duration": 120},
    {"name": "Маникюр",     "price": 1200, "duration": 60},
    {"name": "Педикюр",     "price": 1500, "duration": 75},
]

MASTERS = ["Анна", "Мария", "Ольга"]

TIME_SLOTS = ["10:00", "11:30", "13:00", "14:30", "16:00", "17:30"]
