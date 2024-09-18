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
    def display_own_grid(self):
        own_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.own_grid) ###
        return f"Your grid:\n{own_grid}\n"
    def display_opp_grid(self):
        opp_grid = '\n'.join(' '.join(str(cell) for cell in row) for row in self.opp_grid) ###
        return f"Opponent's grid:\n{opp_grid}\n"
    def __str__(self):
        return f"{self.display_own_grid}{self.display_opp_grid}"
    def place_ship(self, ship):
        for x, y in ship.coordinates:
            if not (0 <= x < 10 and 0 <= y < 10):
                raise ValueError("Ship coordinates out of bounds.")
            if self.own_grid[x][y] != "0":
                raise ValueError("Ship placement overlaps with another ship.")
            self.own_grid[x][y] = 8
    def receive_attack(self, position, attacker):
        x, y = position
        if (self.own_grid[x][y] == "H") or (self.own_grid == "M"): return "ALREADY HITTED"
        elif self.own_grid[x][y] == 1:
            self.own_grid[x][y] = "H"
            attacker[x][y] = "H"
            return "HIT"
        else:
            self.own_grid[x][y] = "M"
            attacker[x][y] = "M"
            return "MISS"
    def check_sunk_status(self, ship):
        if all(self.own_grid[x][y] == "H" for x, y in ship.coordinates): return True
        else: return False

class Player():
    def __init__(self, player = 0): # 0 is user | 1 for machine
        self.player = player
        self.ships = []
        self.grid = Gameboard(self.ships)
        self.attack_record = []
    def get_coordinate(self):
        if self.player:
            x, y = random.randint(1,10), random.randint(1,10)
            return x, y
        else: # Add
            while True:
                x = int(input("Enter starting x-coordinate (1-10): "))
                y = int(input("Enter starting y-coordinate (1-10): "))
                if (not (x in range(1, 10)) or not (y in range(1, 10))): continue
                else: return x - 1, y - 1
    def input_ships(self):
         for ship_length in [2, 3, 3, 4, 5]:
            print(f"Placing ship of length {ship_length}:")
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
                if x + (ship_length - 1) * delta_x >= 10 or y + (ship_length - 1) * delta_y >= 10:
                    print("Ship placement goes out of bounds. Try again.")
                    continue

                coordinates = [(x + i * delta_x, y + i * delta_y) for i in range(ship_length)]

                if any((x + i * delta_x, y + i * delta_y) in [(coord[0], coord[1]) for ship in self.ships for coord in ship.coordinates] for i in range(ship_length)):
                    print("Ship placement overlaps with another ship. Try again.")
                    continue

                try:
                    ship_input = Ship(coordinates, ship_length)
                    self.ships.append(ship_input)
                    self.grid.place_ship(ship_input)

                    print("Your battlefield: ")
                    for i in self.grid.own_grid:
                        print(i)
                    print("\n")

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
    def attack(self, defender, coordinates): ###
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

    inning = 1
    while user and machine:

        if inning % 2 != 0:
            print("Your battlefield: \n")
            for i in user.grid.own_grid:
                print(i)
            print("Opponent's battlefield accordint to your attacks: \n")
            for i in user.grid.opp_grid:
                print(i)
            print(user.grid)

            print("ATTACK!")
            result = user.attack(machine, user.attack_coordinates())
            print(f"The result was a... {result}")
            if result == "HIT":
                print("You have another opportunity.")
                continue
            else: inning += 1
        else:
            print("The enemy is attacking...")
            result = machine.attack(user, machine.attack_coordinates())
            print(f"The result of enemy's attack was a... {result}")
            if result == "HIT":
                print("The enemy has another opportunity.")
                continue
            else: inning += 1
    print("The game is over. The enemy won.")
    if user == False:
        print("You were defeated.")
    elif machine == False:
        print("YOU WON!!!")

if __name__ == "__main__":
    main()

# YES