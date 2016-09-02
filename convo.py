"""The Conversation Module
- Conversation Init
- contains functions for serializing and deserializing Convos
"""

import uuid
from datetime import datetime

class Conversation:
    """Creates an instance of a conversation on instantiation"""
    def __init__(self, allowed_users=None, public_status=True, ):
        """Arguments:
        - self - the Chirp class, itself
        - allowed_users - two user_ids for users allowed to access a private convo
        - public_status - whether or not a conversation is public
        """

        self.allowed_users = allowed_users
        self.public_status = public_status
        # creates a new, unique uuid and saves it as a string instead of a uuid object
        self.uuid = str(uuid.uuid4())
        self.timestamp = datetime.now()
