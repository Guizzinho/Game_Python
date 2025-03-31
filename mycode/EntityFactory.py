import random

from mycode.Const import WIN_WIDTH, WIN_HEIGHT
from mycode.Enemy import Enemy
from mycode.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0), damage=0):
        match entity_name:
            case 'player':
                return Player('player', (position[0], position[1]))
            case 'enemy1':
                return Enemy('Onre', (position[0], position[1]),damage)
            case 'enemy2':
                return Enemy('Yurei', (position[0], position[1]), damage)
            case 'enemy3':
                return Enemy('Gotoku', (position[0], position[1]), damage)
