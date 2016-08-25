import uuid
import pickle
from datetime import datetime

class Chirp:
  """Creates an instance of a chirp on instantiation"""
  def __init__(self, user_id, convo_id, chirp_text):
    """Arguments:
    - self - the Chirp class, itself
    - user_id - foreign id from user creating the chirp, passed in either from new_chirp functions or chirp replies in menus.py
    - convo_id - foreign id from associated conversation, passed in from new_chirp functions in menus.py
    - chirp_text - text of chirp passed in from new_chirp functions or chirp replies in menus.py
    """

    self.user_id = user_id
    self.convo_id = convo_id
    self.text = chirp_text
    # creates a new, unique uuid and saves it as a string instead of a uuid object
    self.uuid = str(uuid.uuid4())
    self.timestamp = datetime.now()

def deserialize_chirps():
  """deserializes the chirps.txt file"""

  # will load last dump (which is entire serialized file)
  try:
    chirps_file = open('chirps.txt', 'rb')
    chirps = pickle.load(chirps_file)
  # creates an empty dict as chirps if chirps.txt is empty
  except EOFError:
    chirps = {}
  return chirps

def serialize_chirps(chirps):
  """serializes chirps to the chirps.txt file

  Arguments:
  - chirps - global variable from menus.py containing deserialized and updated chirps
  """

  # re-writes the whole chirps.txt file with whatever is currently being held in chirps
  chirps_file = open('chirps.txt', 'wb')
  pickle.dump(chirps, chirps_file)
