from dotenv import load_dotenv
import os

load_dotenv()

SCHEDULE_PATH = os.getenv("SCHEDULE")
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
