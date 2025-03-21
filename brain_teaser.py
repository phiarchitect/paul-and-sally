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
        self.asked = 0

    def find_possible_pairs(self):
        # Initial factor pairs for P
        for i in range(1, int(self.P**0.5) + 1):
            if self.P % i == 0:
                self.possible_pairs.append((i, self.P // i))

    def knows_numbers(self):
        return len(self.possible_pairs) == 1

    def eliminate_pairs(self, pairs_to_eliminate):
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]

    def does_not_know_numbers(self):
        self.asked += 1
        if self.asked == 1:
            return True  # Paul doesn't know on the first turn

        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            temp_sally = Sally(pair[0] + pair[1])
            if temp_sally.knows_numbers():
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)
        return not self.knows_numbers()

    def get_numbers(self):
        if self.knows_numbers():
            return self.possible_pairs[0]
        else:
            return None

class Sally:
    def __init__(self, S):
        self.S = S
        self.possible_pairs = []  # List of (a, b) tuples
        self.find_possible_pairs()
        self.initial_elimination()
        self.asked = 0

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

    def does_not_know_numbers(self):
        self.asked += 1
        if self.asked == 1:
            self.initial_elimination()
            return True # Sally doesn't know on the first turn (after initial elimination)

        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            temp_paul = Paul(pair[0] * pair[1])
            if temp_paul.knows_numbers():
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)
        return not self.knows_numbers()

    def get_numbers(self):
        if self.knows_numbers():
            return self.possible_pairs[0]
        else:
            return None
class Tester:
    def __init__(self):
        self.a = random.randint(2, 19)  # Numbers greater than 1
        self.b = random.randint(2, 19)
        self.P = self.a * self.b
        self.S = self.a + self.b
        self.paul = Paul(self.P)
        self.sally = Sally(self.S)


    def run_conversation(self):
        turn = 0
        while True:
            turn += 1
            print(f"Turn {turn}:")

            paul_still_doesnt_know = self.paul.does_not_know_numbers()
            if paul_still_doesnt_know:
                print(f"  Paul's possible pairs: {self.paul.possible_pairs}")
            else:
                print("Paul now knows the numbers")
                if self.sally.knows_numbers():
                    print(f"Paul: The numbers are {self.paul.possible_pairs[0]}")
                    return True
                else:
                    print("Paul and Sally could not determine the numbers.")
                    return False


            sally_still_doesnt_know = self.sally.does_not_know_numbers()

            if sally_still_doesnt_know:
                print(f"  Sally's possible pairs: {self.sally.possible_pairs}")
            else:
                print("Sally now knows the numbers")
                if self.paul.knows_numbers():
                    print(f"Paul: The numbers are {self.paul.possible_pairs[0]}")
                    return True
                else:
                    print("Paul and Sally could not determine the numbers.")
                    return False

            if not paul_still_doesnt_know and not sally_still_doesnt_know:
                break;

        if self.paul.knows_numbers() and self.sally.knows_numbers():
            print(f"Paul: The numbers are {self.paul.possible_pairs[0]}")
            return True

        print("Paul and Sally could not determine the numbers.")
        return False

# Main execution block
tester = Tester()
tester.run_conversation()
