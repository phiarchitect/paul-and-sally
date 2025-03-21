import random

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

class Tester:
    def __init__(self):
        self.a = random.randint(2, 19)  # Numbers greater than 1
        self.b = random.randint(2, 19)
        self.P = self.a * self.b
        self.S = self.a + self.b
        self.paul = Paul(self.P)
        self.sally = Sally(self.S)
        print(f"The secret numbers are: {self.a} and {self.b}")

    def run_conversation(self):

        print("Paul: I don't know the numbers.")
        print(f"  Paul's possible pairs: {self.paul.possible_pairs}")
        if self.paul.knows_numbers():
            print("Paul found the answer too early")
            return False

        paul_knows = self.paul.knows_numbers()

        print("Sally: I don't know the numbers.")
        print(f"  Sally's possible pairs: {self.sally.possible_pairs}")
        if self.sally.knows_numbers():
            print("Sally found the answer too early")
            return False
        
        sally_knows = self.sally.knows_numbers()

        # Sally eliminates pairs where both are prime *after* Paul says he doesn't know
        # Because if both were prime, Paul *would* know
        self.sally.initial_elimination()
        print(f"  Sally's possible pairs after initial elimination: {self.sally.possible_pairs}")

        # Iterate while neither knows the answer
        turn = 0
        while (not paul_knows or not sally_knows) and turn < 7:
            turn += 1
            # Paul's turn to eliminate
            if not paul_knows:
                pairs_to_eliminate = []
                for paul_pair in self.paul.possible_pairs:
                    temp_sally = Sally(paul_pair[0] + paul_pair[1])
                    if temp_sally.knows_numbers():
                        pairs_to_eliminate.append(paul_pair)
                self.paul.eliminate_pairs(pairs_to_eliminate)
                print(f"Paul Turn {turn}:")
                print(f"  Paul's possible pairs: {self.paul.possible_pairs}")
                paul_knows = self.paul.knows_numbers()
                if paul_knows:
                    print("Paul now knows the numbers")


            # Sally's turn to eliminate
            if not sally_knows:
                pairs_to_eliminate = []
                for sally_pair in self.sally.possible_pairs:
                    temp_paul = Paul(sally_pair[0] * sally_pair[1])
                    if temp_paul.knows_numbers():
                        pairs_to_eliminate.append(sally_pair)
                self.sally.eliminate_pairs(pairs_to_eliminate)
                print(f"Sally Turn {turn}:")
                print(f"  Sally's possible pairs: {self.sally.possible_pairs}")
                sally_knows = self.sally.knows_numbers()
                if sally_knows:
                    print("Sally now knows the numbers")

        if self.paul.knows_numbers() and self.sally.knows_numbers():
            print(f"Paul: The numbers are {self.paul.possible_pairs[0]}")
            return True

        print("Paul and Sally could not determine the numbers.")
        return False

# Main execution block
tester = Tester()
tester.run_conversation()

