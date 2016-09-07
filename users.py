"""The User Module
- User Init
- contains functions for serializing and deserializing Users
"""

import uuid

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
