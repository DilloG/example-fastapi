from dotenv import load_dotenv
import os

load_dotenv(".env")
print(os.getenv("database_password"))