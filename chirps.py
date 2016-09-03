"""The Chirp Module
- Chirp Init
- contains functions for serializing and deserializing Chirps
"""

import uuid
from datetime import datetime

class Chirp:
    """Creates an instance of a chirp on instantiation"""
    def __init__(self, user_id, convo_id, chirp_text):
        """Arguments:
        - self - the Chirp class, itself
        - user_id - foreign id from user creating the chirp
        - convo_id - foreign id from associated conversation
        - chirp_text - text of chirp passed in from new_chirp functions or chirp replies in menus.py
        """
        self.user_id = user_id
        self.convo_id = convo_id
        self.text = chirp_text
        # creates a new, unique uuid and saves it as a string instead of a uuid object
        self.uuid = str(uuid.uuid4())
        self.timestamp = datetime.now()
