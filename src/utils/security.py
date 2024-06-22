import sys
import base64
import string
import random
import secrets
import hashlib

from itertools import cycle
from dataclasses import dataclass

@dataclass
class HashType:
    MD5 = hashlib.md5
    SHA1 = hashlib.sha1
    SHA256 = hashlib.sha256
    SHA384 = hashlib.sha384
    SHA512 = hashlib.sha512
    
class Hashing:
    @staticmethod
    def calculate_message_hash(data: str, hashtype: HashType = HashType.SHA512) -> str:
        hasher = hashtype(data.encode('utf-8'))
        return hasher.digest().hex()

class Passwords:
    @staticmethod
    def derive_hash(seed):
        """Generates a random hash based on a seed."""
        generator = random.Random(seed)
        values = [str(generator.random()) for _ in range(8192)]
        return Hashing.calculate_message_hash('-'.join(values)) # The delimiter ('-') should ALWAYS BE A CONSTz.

    """Contains a collection of text generation utilities such as random id and cid strings."""
    @staticmethod
    def generate_id(length: int = 10,  use_sample: bool = False) -> str:
        """
        Returns an alphanumeric identifier based on a given length and random sampling, if desired.

        Parameters
        ----------
        length : Optional[:class:`int`]
            The length of the identifier to be generated.
        use_sample : Optional[:class:`bool`]
            Use :func:`random.sample()` instead of :func:`secrets.choice()` on available characters.

        Returns
        ----------
        :class:`str`
            The generated id of a specified length.
        """
        characters = string.ascii_letters + string.digits
        if use_sample:
            return random.sample(characters, length)
        else:
            return ''.join((secrets.choice(characters) for i in range(length)))

    @staticmethod
    def generate_cid(length: int = 64) -> str:
        """
        Returns a Base64 encoded cryptographically strong random identifier.
        
        Parameters
        ----------
        length : Optional[:class:`int`]
            The length of the identifier to be generated.

        Returns
        ----------
        :class:`str`
            The generated cryptographic id of a specified length.
        """
        delimiters = {1:'-', 2:';', 3:':', 4:'/', 5:'!', 6:'@', 7:'#', 8:'$', 9:'%', 10:'&', 11:'*', 12:'|'}
        generated_id = Passwords.generate_id(length)
        with_entropy = Hashing.calculate_message_hash(f'{delimiters[random.randint(1, len(delimiters.items()))]}'.join([f'{char}{delimiters[random.randint(1, len(delimiters.items()))]}' for char in generated_id]))
        return base64.b64encode(str.encode(with_entropy)).decode('utf-8')
    
    @staticmethod
    def generate_salt():
        return Passwords.generate_cid()
    
    @staticmethod
    def generate_pepper(text, key):
        encoded_input = str(text).encode('utf-8')
        encoded_key = str(key).encode('utf-8')
        derived_string = Passwords.derive_hash(f"{encoded_input}{encoded_key}")
        reversed_string = ''.join(list(reversed(derived_string)))
        hashed_string = Hashing.calculate_message_hash(reversed_string)
        rehashed_string = hashlib.pbkdf2_hmac('sha512', key.encode('utf-8'), hashed_string.encode('utf-8'), 100000).hex()
        pepper = base64.b64encode(str.encode(rehashed_string)).decode('utf-8')
        return pepper