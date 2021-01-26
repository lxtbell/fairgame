import os
from config import Config as Cfg
import stdiomask

from utils.encryption import load_encrypted_config, create_encrypted_config
from utils.logger import log

GLOBAL_CONFIG_FILE = "config/fairgame.conf"
AMAZON_CREDENTIAL_FILE = "config/amazon_credentials.json"


def await_credential_input():
    username = input("Amazon login ID: ")
    password = stdiomask.getpass(prompt="Amazon Password: ")
    return {
        "username": username,
        "password": password,
    }


def get_credentials(credentials_file, encrypted_pass=None):
    if os.path.exists(credentials_file):
        credential = load_encrypted_config(credentials_file, encrypted_pass)
        return credential["username"], credential["password"]
    else:
        log.info("No credential file found, let's make one")
        log.info("NOTE: DO NOT SAVE YOUR CREDENTIALS IN CHROME, CLICK NEVER!")
        credential = await_credential_input()
        create_encrypted_config(credential, credentials_file)
        return credential["username"], credential["password"]


class GlobalConfig:
    def __init__(self) -> None:
        super().__init__()
        log.info("Initializing Global configuration...")
        # Load up the global configuration
        # See http://docs.red-dove.com/cfg/python.html#getting-started-with-cfg-in-python for how to use Config
        self.global_config = Cfg(GLOBAL_CONFIG_FILE)
        self.fairgame_config = self.global_config.get("FAIRGAME")
        self.profile_path = None
        self.get_browser_profile_path()

    def get_amazon_config(self, encryption_pass=None):
        log.info("Initializing Amazon configuration...")
        # Load up all things Amazon
        amazon_config = self.global_config["AMAZON"]
        amazon_config["username"], amazon_config["password"] = get_credentials(
            AMAZON_CREDENTIAL_FILE, encryption_pass
        )
        return amazon_config

    def get_browser_profile_path(self):
        if not self.profile_path:
            self.profile_path = os.path.join(
                os.path.dirname(os.path.abspath("__file__")),
                self.global_config["FAIRGAME"].get("profile_name", ".profile-amz"),
            )
        return self.profile_path
