import uuid

class User:
  def __init__(self, name, screenname):
    self.name = name
    self.screenname = screenname
    self.uuid = uuid.uuid4()

  # def __str__(self):
  #   return 'name: {}, username: {}, uuid: {}'.format(self.name, self.screenname, self.uuid)



