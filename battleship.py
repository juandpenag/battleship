import random

class Ship():
    def __init__(self, coordinates, length):
        self.coordinates = coordinates
        self.length = length
        self.sunk = False
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
        own_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.own_grid)
        opp_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.opp_grid)
        return f"Your grid:\n{own_grid}\n\nOpponent's grid:\n{opp_grid}"
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
    def check_sunk_status(self, ship): 
        if all(self.own_grid[x][y] == "X" for x, y in ship.coordinates): return True
        else: return False

class Player():
    def __init__(self, player = 0): # 0 is user | 1 for machine
        self.player = player
        self.ships = []
        self.grid = Gameboard(self.ships)
        self.attack_record = []
    def get_coordinate(self):
        if self.player: 
            x, y = random.randint(0,9), random.randint(0,9)
        else: # Add 
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
            while True:
                
                while True:
                    orientation = random.randint(0,1) if self.player else int(input("Enter orientation (0 for horizontal, 1 for vertical): "))
                    if orientation in [0, 1]:
                        break
                    else: 
                        print("Invalid orientation value. Try again.")
                        continue
                    
                x, y = self.get_coordinate()
                if (not (x in range(0, 10)) or not (y in range(0, 10))): ###
                    print("Given coordinates out of bounds. Try again.")
                    continue
            
                delta_x, delta_y = (1, 0) if orientation == 0 else (0, 1)
                if x + (ship.length - 1) * delta_x >= 10 or y + (ship.length - 1) * delta_y >= 10:
                    print("Ship placement goes out of bounds. Try again.")
                    continue

                coordinates = [(x + i * delta_x, y + i * delta_y) for i in range(ship.length)]
                    
                if any((x + i * delta_x, y + i * delta_y) in [(coord[0], coord[1]) for ship in self.ships for coord in ship.coordinates] for i in range(ship.length)):
                    print("Ship placement overlaps with another ship. Try again.")
                    continue

                try:
                    ship_input = ship(coordinates)
                    self.ships.append(ship_input)
                    break
                except ValueError as e:
                    print(f"Error placing ship: {e}")
    def attack_coordinates(self): 
        while True:
            x, y = self.get_coordinate()
            if (x, y) in self.attack_record: 
                print("You already attacked there. Try again.")
                continue
            else: 
                self.attack_record.append((x, y))
                return x, y
    def attack(self, opponent, coordinates): 
        result = opponent.grid.receive_attack(coordinates)
        return result
    def __bool__(self):
        for ship in self.ships:
            ship.sunk = self.grid.check_sunk_status(ship)
        if all(ship.sunk for ship in self.ships): return True
        else: return False

def main():
    print("This is BATTLESHIP! recreated in Python.")
    user, machine = Player(), Player(1)

    user.input_ships()
    machine.input_ships()

    inning = 1
    round = 1
    while user and machine:
        print(f"Round {round}")
        if inning % 2 != 0:
            print(user.grid)
            print("Attack!")
            result = user.attack(machine, user.attack_coordinates())
            print(f"The result was a... {result}")
            if result != "HIT":
                print("You have another opportunity in this round.")
                inning += 1
        else:
            print("The enemy is attacking.")
            result = machine.attack(user, machine.attack_coordinates())
            print(f"The result of enemy's attack was a... {result}")
            if result != "HIT":
                print("The enemy has another opportunity in this round.")
                inning += 1
        round += 1
    print("The game is over.")
    if user == False:
        print("You were defeated.")
    elif machine == False:
        print("YOU WON!!!")

if __name__ == "__main__":
    main()