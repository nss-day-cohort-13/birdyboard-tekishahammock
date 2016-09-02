"""The User Module
- User Init
- contains functions for serializing and deserializing Users
"""

import uuid
import pickle

class User:
    """Creates an instance of user on instantiation"""
    def __init__(self, name, screenname):
        """Arguments:
        - self - the User class, itself
        - name - contents of name variable from menus.py in new_user_menu function
        - screenname - contents of screenname variable from menus.py in new_user_menu function
        """

        self.name = name
        self.screenname = screenname
        # creates a new, unique uuid and saves it as a string instead of a uuid object
        self.uuid = str(uuid.uuid4())

def deserialize_users():
    """deserializes the users.txt file"""

    # will load last dump (which is entire serialized file)
    try:
        user_file = open('users.txt', 'rb')
        user_list = pickle.load(user_file)
    # creates an empty dict as user_list if users.txt is empty
    except EOFError:
        user_list = {}
    return user_list

def serialize_users(user_list):
    """serializes user_list to the users.txt file

    Arguments:
    - user_list - global variable from menus.py containing deserialized and updated user_list
    """

    # re-writes the whole users.txt file with whatever is currently being held in user_list
    user_file = open('users.txt', 'wb')
    pickle.dump(user_list, user_file)
