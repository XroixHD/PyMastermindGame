import math
import os
import sys
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def get_file_path(file):
    """ Get file path of file
    :param file: the filename
    """
    return os.path.join(os.path.dirname(sys.argv[0]), "res", file)


class Config:
    """ Saves state
    """

    FILE_NAME = get_file_path("../config.json")
    TEMPLATE = {
        "last_code": "",
        "last_count": 0,
        "history": [
            # {"code": [1, 0, 3, 4, 3, 2], "answer": "XXXOOO"}
        ]
    }

    def __init__(self, root):
        """ Initialize
        :param root: the root tk window
        """
        self.root = root
        self.data = {}

        self.load_file()
        self.write_file()

    def __getitem__(self, item):
        """ Get item from data attribute
        :param item: item
        """
        return self.data[item]

    def load_file(self):
        """ Load a existing config file
        """
        try:
            with open(self.FILE_NAME, "a+") as f:
                f.seek(0)

                if data := json.load(f):
                    print("Loading config")
                    self.data = data

                else:
                    print("Loading template, config is empty!")
                    self.data = self.TEMPLATE

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("Couldn't open config")
            self.data = self.TEMPLATE

    def write_file(self):
        """ Write to the config file and thus, save changes
        """
        with open(self.FILE_NAME, "w+") as f:
            json.dump(self.data, f, indent=4)

    def save_state(self):
        """ Saves all state information
        """
        self.data["last_code"] = self.root.mastermind.secret_code
        self.data["last_count"] = self.root.mastermind.count
        self.data["history"] = self.root.mastermind.history
        self.write_file()
