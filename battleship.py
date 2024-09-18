"""
    Coordinates cannot be the same 
    Add attack record 
    Add attack_coordinates into Player class
    Add random input to machine 
    If HIT, attack again
    Review raised errors 
    Check coordinates input
    Consider if self.sunk is necessary
    Move ship status checking to Gameboard, and clarify the __bool__ method.
    Refactor attack to avoid recursion.
    Additionally, streamline the input_ships validation process.
Beauty up the output in terminal
    Simplify the game loop and remove the redundant stage variable.
    Create a class function in Player to receive coordinates
"""

import random

class Ship():
    def __init__(self, coordinates, length):
        self.coordinates = coordinates
        self.length = length
        self.sunk = True
    def __iter__(self):
        return iter(self.coordinates)
    def __bool__(self): 
        return self.sunk
        
class Two_Long(Ship):
    def __init__(self, coordinates):
        super().__init__(coordinates, 2)
class Three_Long(Ship):
    def __init__(self, coordinates):
        super().__init__(coordinates, 3)
class Four_Long(Ship):
    def __init__(self, coordinates):
        super().__init__(coordinates, 4)
class Five_Long(Ship):
    def __init__(self, coordinates):
        super().__init__(coordinates, 5)

class Gameboard():
    def __init__(self, ships):
        self.own_grid = [[0 for j in range(10)] for i in range(10)]
        self.opp_grid = [[0 for j in range(10)] for i in range(10)]
        self.own_ships = ships
    def __str__(self):
        own_grid = [self.own_grid[i] for i in range(len(self.own_grid))]
        opp_grid = [self.opp_grid[i] for i in range(len(self.opp_grid))]
        return (own_grid, opp_grid) ###
    def place_ship(self, ship):
        for x, y in ship.coordinates:
            if not (0 <= x < 10 and 0 <= y < 10):
                raise ValueError("Ship coordinates out of bounds.")
            if self.own_grid[x][y] != 0:
                raise ValueError("Ship placement overlaps with another ship.")
            self.own_grid[x][y] = 1
    def receive_attack(self, position): 
        x, y = position
        if self.own_grid[x][y] == "X": return "ALREADY HITTED"
        elif self.own_grid[x][y] == 1:
            self.own_grid[x][y] = "X"
            self.opp_grid[x][y] = "X"
            return "HIT"
        else: 
            self.own_grid[x][y] = "O"
            self.opp_grid[x][y] = "O"
            return "MISS"
    def sunk_ships(self, ship): 
        if all(self.own_grid[x][y] == "X" for x, y in ship.coordinates): return False
        else: return True

class Player():
    def __init__(self, player = 0): # 0 is user | 1 for machine
        self.player = player
        self.active = self.bool()
        self.grid = Gameboard()
        self.ships = []
        self.attack_record = []
    def get_coordinate(self):
        if self.player: 
            x, y = random.randint(0,9), random.randint(0,9)
        else:
            while True:
                x = int(input("Enter starting x-coordinate (1-10): ")) - 1
                y = int(input("Enter starting y-coordinate (1-10): ")) - 1
                if (not (x in range(0, 9)) or not (y in range(0, 9))): continue
                else: return x, y
    def place_ships(self): 
        for ship in self.ships:
            self.grid.place_ship(ship) 
    def input_ships(self): 
         for ship in [Two_Long, Three_Long, Three_Long, Four_Long, Five_Long]:
            print(f"Placing {ship.__name__}:")
            x, y = self.get_coordinate()
            orientation = random.randint(0,1) if self.player else int(input("Enter orientation (0 for horizontal, 1 for vertical): "))
            delta_x, delta_y = (1, 0) if orientation == 0 else (0, 1)
            coordinates = [(x + i * delta_x, y + i * delta_y) for i in range(ship.length)]

            while True: 
                if (not (x in range(0, 9)) or not (y in range(0, 9)) or not (orientation in range(0, 1))): 
                    print(...)
                    continue
                elif any((x + i * delta_x > 9 or y + i * delta_y > 9) for i in range(ship.length)):
                    print(...)
                    continue
                elif set(coordinates).intersection(set(coord for ship in self.ships for coord in ship.coordinates)):
                    print(...)
                    continue
                else: break
            try:
                ship_input = ship(coordinates)
                self.ships.append(ship_input)
            except ValueError as e:
                print(f"Error placing ship: {e}")
    def attack_coordinates(self): 
        while True:
            x, y = self.get_coordinate()
            if (x, y) in self.attack_record: 
                print(...)
                continue
            else: 
                self.attack_record.append((x, y))
                return x, y
    def attack(self, opponent, coordinates): 
        result = opponent.grid.receive_attack(coordinates)
        return result
    def __bool__(self):
        for ship in self.ships:
            ship.sunk = self.grid.sunk_ships(ship)
        if all(ship.sunk for ship in self.ships): return False
        else: return True



def main():
    user = Player()
    machine = Player(1)

    user.input_ships()
    machine.input_ships()

    while user and machine :
        inning = 1
        while user and machine:
            if inning % 2 != 0:  # User's turn
                result = user.attack(machine, user.attack_coordinates())
                if result != "HIT":
                    inning += 1
            else:  # Machine's turn
                result = machine.attack(user, machine.attack_coordinates())
                if result != "HIT":
                    inning += 1


    if user == False:
        print("Machine wins!")
    elif machine == False:
        print("User wins!")

if __name__ == "__main__":
    main()