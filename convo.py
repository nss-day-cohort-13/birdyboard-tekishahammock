"""The Conversation Module
- Conversation Init
- contains functions for serializing and deserializing Convos
"""

import uuid
import pickle
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

def deserialize_convo():
    """deserializes the convo.txt file"""

    # will load last dump (which is entire serialized file)
    try:
        convo_file = open('convo.txt', 'rb')
        convo_list = pickle.load(convo_file)
        # creates an empty dict as convo_list if convo.txt is empty
    except EOFError:
        convo_list = {}
    return convo_list

def serialize_convo(convo_list):
    """serializes convo_list to the convo.txt file

    Arguments:
    - convo_list - global variable from menus.py containing deserialized and updated conversations
    """
    print("Convo_list:", convo_list)

    # re-writes the whole convo.txt file with whatever is currently being held in chirps
    convo_file = open('convo.txt', 'wb')
    pickle.dump(convo_list, convo_file)
