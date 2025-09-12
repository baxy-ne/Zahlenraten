from models.user import User
import random
class Game:
  def __init__(self, aktuelle_versuche):
    self.aktuelle_versuche = aktuelle_versuche
    self.random_number = random.randint(1, 100)