from dotenv import load_dotenv
import os

def getCredentials():
    load_dotenv(dotenv_path = "./config/.env-shared", verbose = True, override = True)
    
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL")
    MANAGER_EMAIL  = os.getenv("MANAGER_EMAIL")
    
    print(os.getenv("ADMIN_PASSWORD"))
    print(os.getenv("ADMIN_EMAIL"))
    print(os.getenv("MANAGER_EMAIL"))
    
    return ADMIN_EMAIL, ADMIN_PASSWORD, MANAGER_EMAIL
