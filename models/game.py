from models.user import User
class Game:
  def __init__(self, aktuelle_versuche, random_number, user: User):
    self.aktuelle_versuche = aktuelle_versuche
    self.random_number = random_number
    self.user = user