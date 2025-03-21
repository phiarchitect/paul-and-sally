def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

class Paul:
    def __init__(self, P):
        self.P = P
        self.possible_pairs = []  # List of (a, b) tuples
        self.find_possible_pairs()

    def find_possible_pairs(self):
        # Initial factor pairs for P
        for i in range(1, int(self.P**0.5) + 1):
            if self.P % i == 0:
                self.possible_pairs.append((i, self.P // i))

    def knows_numbers(self):
        return len(self.possible_pairs) == 1

    def eliminate_pairs(self, pairs_to_eliminate):
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]

    def receive_sally_info(self, sally_potential_pairs):
        #sally potential pairs is a list of valid (a,b)
        valid_pairs = []
        for pair in self.possible_pairs:
            possible_sums = []
            for sally_pair in sally_potential_pairs:
                possible_sums.append(sally_pair[0] + sally_pair[1])
            if pair[0] + pair[1] in possible_sums:
                valid_pairs.append((pair[0] * pair[1], pair))

        new_pairs = []
        products = []
        for pair in valid_pairs:
            if pair[0] not in products:
                products.append(pair[0])
                new_pairs.append(pair[1])
            else:
                #remove any existing
                new_pairs = [p for p in new_pairs if (p[0] * p[1]) != pair[0]]
        self.possible_pairs = new_pairs


class Sally:
    def __init__(self, S):
        self.S = S
        self.possible_pairs = []  # List of (a, b) tuples
        self.find_possible_pairs()
        self.initial_elimination()

    def find_possible_pairs(self):
        # Initial pairs that sum to S
        for i in range(1, self.S // 2 + 1):
            self.possible_pairs.append((i, self.S - i))

    def knows_numbers(self):
        return len(self.possible_pairs) == 1

    def eliminate_pairs(self, pairs_to_eliminate):
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]

    def initial_elimination(self):
        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            if is_prime(pair[0]) and is_prime(pair[1]):
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)

    def receive_paul_info(self, paul_potential_pairs):
        #sally potential pairs is a list of valid (sum, (a,b))
        valid_pairs = []

        for pair in self.possible_pairs:
            possible_products = []
            for paul_pair in paul_potential_pairs:
                possible_products.append (paul_pair[0] * paul_pair[1])
            if pair[0] * pair[1] in possible_products:
                valid_pairs.append((pair[0] + pair[1], pair))

        new_pairs = []
        sums = []
        for pair in valid_pairs:
            if pair[0] not in sums:
                sums.append(pair[0])
                new_pairs.append(pair[1])
            else:
              #remove any existing
              new_pairs = [p for p in new_pairs if (p[0] + p[1]) != pair[0]]
        self.possible_pairs = new_pairs

class Tester:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.P = a * b
        self.S = a + b
        self.paul = Paul(self.P)
        self.sally = Sally(self.S)

    def run_conversation(self):
        print("Paul: I don't know the numbers.")
        if self.paul.knows_numbers():
            print (f"Paul found the answer too early {self.paul.possible_pairs}")
            return False

        print("Sally: I don't know the numbers.")
        self.sally.receive_paul_info(self.paul.possible_pairs)  # Pass Paul's info to Sally
        if self.sally.knows_numbers():
            print (f"Sally found the answer too early {self.sally.possible_pairs}")
            return False

        print("Paul: I still don't know the numbers.")
        self.paul.receive_sally_info(self.sally.possible_pairs) # Pass Sally's info to Paul
        if self.paul.knows_numbers():
            print (f"Paul found the answer too early {self.paul.possible_pairs}")
            return False

        print("Sally: I still don't know the numbers.")
        self.sally.receive_paul_info(self.paul.possible_pairs)  # Pass Paul's updated info to Sally
        if self.sally.knows_numbers():
            print (f"Sally found the answer too early {self.sally.possible_pairs}")
            return False

        print("Paul: Now I know the numbers.")
        if self.paul.knows_numbers():
            print(f"Paul: The numbers are {self.paul.possible_pairs[0]}")
            return True

        print("Paul could not determine the numbers.")
        return False

# Main execution block
for a in range(1, 20):
    for b in range(a, 20):  # Avoid duplicates (a, b) and (b, a)
        tester = Tester(a, b)
        if tester.run_conversation():
            print(f"Solution found for a={a}, b={b}")

