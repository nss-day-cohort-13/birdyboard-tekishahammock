import uuid
import pickle
import inspect

class User:
  """Creates an instance of user on instantiation"""
  def __init__(self, name, screenname):
    self.name = name
    self.screenname = screenname
    self.uuid = str(uuid.uuid4())

  # Testing returned values of instantiated User object:
  # def __str__(self):
  #   return 'name: {}, username: {}, uuid: {}'.format(self.name, self.screenname, self.uuid)

def deserialize_users():
  try:
    user_file = open('users.txt', 'rb')
    user_list = pickle.load(user_file)
  except EOFError:
    user_list = {}
  return user_list

def serialize_users(user_list):
  user_file = open('users.txt', 'wb')
  pickle.dump(user_list, user_file)






