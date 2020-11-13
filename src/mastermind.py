import math
import random
import binascii

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Mastermind:
    """ Mastermind game logic
    """

    COLORS = ["lila", "blau", "gelb", "rot", "gruen", "orange"]
    COLOR_CODES = {"lila": "violet", "blau": "blue", "gelb": "yellow", "rot": "red", "gruen": "green", "orange": "orange"}

    def __init__(self, root, *, secret_code=None, _i=0, history=None):
        """ Initialize
        :param root: the root window obj
        """
        self.root = root

        self.pressed = []
        self.history = history if history else []

        self.secret_code = secret_code if secret_code else self.generate_normal_code()

        # Keeps track of current field and tries
        self._i = _i
        self.len = len(self.COLORS)

    @classmethod
    def from_config(cls, root, config):
        """ Generates a new Mastermind instance from a config state
        :returns: instance
        """
        return cls(root, secret_code=config["last_code"], _i=(config["last_count"] * len(cls.COLORS)), history=config["history"])

    @classmethod
    def generate_normal_code(cls) -> list:
        """ DEBUG TODO
        """
        return [random.choice(cls.COLORS) for _ in cls.COLORS]
        # return random.sample(cls.COLORS, len(cls.COLORS))

    @classmethod
    def generate_code_hash(cls) -> str:
        """ Generate a hash of the secret code
        :returns: (str) the hash
        """
        temp = (",".join(random.sample(list(map(str.__call__, range(len(cls.COLORS)))), len(cls.COLORS)))).encode("utf8")

        digest = hashes.Hash(hashes.SHA256(), default_backend())
        digest.update(temp)

        return binascii.hexlify(digest.finalize()).decode("utf8")

    @property
    def index(self) -> int:
        """ Get the index, idk any more how it gets calculated ._.
        :returns: (int) the index
        """
        return self._i - self.len * math.floor((self._i - 1) / self.len) - 1

    @property
    def count(self) -> int:
        """ Get the number of how many times it was guessed
            based on _i and len
        :returns: (int) the count
        """
        return math.floor(self._i / self.len)

    def press(self, color: str) -> int:
        """ 'Press' a color
        :param color: the color name
        :returns: the current index
        """
        self.pressed.append(color)
        self._i += 1

        return self.index

    def evaluate(self) -> list:
        """ Evaluates the provided code
        """
        answer_list = []

        # 0 -> X, 1 -> BLANK, 2 -> O
        for i, answer in enumerate(self.pressed):
            # Correct Color + Position (X)
            if self.secret_code[i] == answer:
                answer_list.append(0)

            # Correct Color (0)
            elif answer in self.secret_code:
                answer_list.append(2)

            # Just for padding
            else:
                answer_list.append(1)

        # for example: X X pad 0
        #              0 0 1   2
        answer_list.sort()

        self.history.append({
            "code": ";".join(self.pressed),
            "answer": "".join("X" * int(x == 0) + "  " * int(x == 1) + "O" * int(x == 2) for x in answer_list)
        })
        self.pressed = []

        return answer_list

    def clear(self):
        """ Clears session and config
        """
        self.pressed = []
        self.history = []
        self._i = 0
        self.secret_code = self.generate_normal_code()
