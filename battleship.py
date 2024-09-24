import random

class Ship():
    def __init__(self, coordinates, length):
        self.coordinates = coordinates
        self.length = length
        self.sunk = False
    def __bool__(self):
        return self.sunk

class Gameboard():
    def __init__(self, ships):
        self.own_grid = [["0" for j in range(10)] for i in range(10)]
        self.opp_grid = [["0" for j in range(10)] for i in range(10)]
        self.own_ships = ships
        
    def __str__(self):
        return f"{self.display_own_grid()}\n{self.display_opp_grid()}"
    
    def display_own_grid(self):
        own_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.own_grid)
        return f"Your battlefield:\n{own_grid}"
    
    def display_opp_grid(self):
        opp_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.opp_grid)
        return f"Opponent's grid:\n{opp_grid}"
  
    def place_ship(self, ship):
        for x, y in ship.coordinates:
            if self.own_grid[y][x] != "0":
                raise ValueError("Ship placement overlaps with another ship.")
            else: self.own_grid[y][x] = 1

    def receive_attack(self, position, attacker):
        x, y = position

        if self.own_grid[y][x] == 1: # If hitted
            self.own_grid[y][x] = "H"
            attacker[y][x] = "H"
            return "HIT"
        else: # if not hitted
            self.own_grid[y][x] = "M"
            attacker[y][x] = "M"
            return "MISS"
        
    def check_sunk_status(self, ship): # Checking if ship's still active
        if all(self.own_grid[y][x] == "H" for x, y in ship.coordinates): return True
        else: return False

class Player():
    def __init__(self, player = 0): # 0 is user, 1 for machine
        self.player = player
        self.ships = []
        self.grid = Gameboard(self.ships)
        self.attack_record = []

    def get_coordinate(self): # Function to get coordinates
        if self.player:
            x, y = random.randint(1,10), random.randint(1,10)
        else:
            while True:
                x = int(input("Enter x-coordinate (1-10): "))
                y = int(input("Enter y-coordinate (1-10): "))
                if (not (x in range(1, 11)) or not (y in range(1, 11))):
                    print("Given coordinates out of bounds. Try again.")
                    continue
                else: break
        return x - 1, y - 1

    def input_ships(self):
         for ship_length in [2, 3, 3, 4, 5]: # The list is the length of each ship
            print(f"Placing ship of length: {ship_length}.")
            while True:

                while True: # Get & Check orientation of ship
                    orientation = random.randint(0,1) if self.player else int(input("Enter orientation (0 for horizontal, 1 for vertical): "))
                    if orientation in [0, 1]:
                        break
                    else:
                        print("Invalid orientation value. Try again.")
                        continue

                x, y = self.get_coordinate() # Get starting coordinate
                delta_x, delta_y = (1, 0) if orientation == 0 else (0, 1) # Variables needed to get all of the coordinates 

                if x + (ship_length - 1) * delta_x >= 10 or y + (ship_length - 1) * delta_y >= 10: 
                    print("Ship placement goes out of bounds. Try again.")
                    continue

                coordinates = [(x + i * delta_x, y + i * delta_y) for i in range(ship_length)] # Getting coordinates

                if any((x + i * delta_x, y + i * delta_y) in [(coord[0], coord[1]) for ship in self.ships for coord in ship.coordinates] for i in range(ship_length)):
                    print("Ship placement overlaps with another ship. Try again.")
                    continue

                try: # Adding ship to self.ships
                    ship_input = Ship(coordinates, ship_length)
                    self.ships.append(ship_input)
                    self.grid.place_ship(ship_input)
                    print(f"{self.grid.display_own_grid()}\n")
                    break
                except ValueError as e:
                    print(f"Error placing ship: {e}")

    def attack_coordinates(self):
        while True:
            x, y = self.get_coordinate()
            if (x, y) in self.attack_record: # Checking if those coordinates where attacked
                print("You already attacked there. Try again.")
                continue
            else:
                self.attack_record.append((x, y))
                return x, y
            
    def attack(self, defender, coordinates):
        result = defender.grid.receive_attack(coordinates, self.grid.opp_grid)
        return result
    
    def __bool__(self):
        for ship in self.ships:
            ship.sunk = self.grid.check_sunk_status(ship)
        if all(ship.sunk == True for ship in self.ships): return False
        else: return True

def main():
    print("This is BATTLESHIP! recreated in Python.")
    user, machine = Player(), Player(1)

    user.input_ships()
    machine.input_ships()

    print("LET'S PLAY!")
    inning = 1
    while user and machine:

        if inning % 2 != 0:
            print(user.grid)
            print("ATTACK!\n")
            result = user.attack(machine, user.attack_coordinates())
            print(f"The result was a... {result}")
            if result == "HIT":
                print("You have another opportunity.")
                continue
            else: inning += 1
        else:
            print("The enemy is attacking...")
            result = machine.attack(user, machine.attack_coordinates())
            print(f"The result of enemy's attack was a... {result}.")
            if result == "HIT":
                print("The enemy has another opportunity.")
                continue
            else: inning += 1

    print("The game is over.")
    if user == False:
        print("You were defeated.")
    elif machine == False:
        print("YOU WON!!!")

if __name__ == "__main__":
    main()
