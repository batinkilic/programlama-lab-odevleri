import random

class Warrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def attack(self):
        pass  # Saldırı işlevi burada tanımlanabilir, alt sınıflarda uygulanacaktır

    def get_representation(self):
        return self.__class__.__name__[0]  # Savaşçıyı temsil eden ilk harfi döndürür

class Knight(Warrior):
    def attack(self):
        print("Knight is attacking!")

class Archer(Warrior):
    def attack(self):
        print("Archer is attacking!")

class Mage(Warrior):
    def attack(self):
        print("Mage is attacking!")

class Player:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.resources = 10
        self.warriors = []

    def add_warrior(self, warrior):
        self.warriors.append(warrior)

    def remove_warrior(self, warrior):
        self.warriors.remove(warrior)

class World:
    def __init__(self, size):
        self.size = size
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def place_initial_guard(self):
        self.grid[0][0] = Guard()

    def print_world(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.grid[row][col]
                if isinstance(cell, Warrior):
                    print(cell.get_representation(), end=" ")
                else:
                    print(cell, end=" ")
            print()  # Bir sonraki satıra geç

class Guard(Warrior):
    def __init__(self):
        # Muhafızın konumu sabittir
        super().__init__(x=0, y=0)

def create_warrior(player, world):
    warrior_type = random.choice([Knight, Archer, Mage])
    x = random.randint(0, world.size - 1)
    y = random.randint(0, world.size - 1)
    warrior = warrior_type(x, y)
    player.add_warrior(warrior)
    world.grid[x][y] = warrior

def initialize_players(num_players):
    colors = ['Red', 'Blue', 'Green', 'Yellow']
    players = [Player(i+1, colors[i]) for i in range(num_players)]
    return players

def main():
    size = int(input("Enter the size of the world (8-32): "))
    if size < 8 or size > 32:
        print("Invalid size! Size must be between 8 and 32.")
        return

    num_players = int(input("Enter the number of players (1-4): "))
    if num_players < 1 or num_players > 4:
        print("Invalid number of players! Must be between 1 and 4.")
        return

    world = World(size)
    world.place_initial_guard()

    players = initialize_players(num_players)
    for player in players:
        world.add_player(player)

    for player in players:
        for _ in range(2):  # Her oyuncu için 2 savaşçı oluşturma
            create_warrior(player, world)

    world.print_world()

if __name__ == "__main__":
    main()
