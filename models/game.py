import random
class Game:
  def __init__(self, user_id, aktuelle_versuche):
    self.user_id = user_id
    self.aktuelle_versuche = aktuelle_versuche
    self.random_number = random.randint(1, 100)