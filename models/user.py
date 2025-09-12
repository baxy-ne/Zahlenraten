from uuid import uuid4
class User:
  def __init__(self, username, password):
    self.user_id = str(uuid4())
    self.username = username
    self.password = password
