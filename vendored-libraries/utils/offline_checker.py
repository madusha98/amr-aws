import os

def check_offline():
    env = os.environ.get("IS_OFFLINE")
    print(env)
    return env == "true"