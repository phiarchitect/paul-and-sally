"""
this code is intended to model this brainteaser:
There are two people, Paul and Sally, both very smart logicians. Paul knows the
product of two natural numbers, greater than zero. He doesn't know the two
natural numbers, just their product. Sally knows the sum of the same two
natural numbers. She doesn't know the natural numbers, just the sum. Paul knows
that Sally knows the sum of the same two natural numbers , and Sally knows that
Paul knows the product of the two natural numbers. Paul says to Sally "I don't
know what the two numbers are." Sally says to Paul "I don't know what the two
nu mbers are either." Paul says to Sally "I still don't know what the two
numbers are." Sally says to Paul "I still don't know what they are either."
Paul then says "Now I know what the two numbers are." What are the 2 numbers?

"""

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
        for i in range(2, int(self.P**0.5) + 1):  # Start from 2
            if self.P % i == 0:
                self.possible_pairs.append((i, self.P // i))

    def knows_numbers(self):
        # Count prime factors of P
        factors = []
        temp_p = self.P
        for i in range(2, int(temp_p**0.5) + 1):
            while temp_p % i == 0:
                factors.append(i)
                temp_p //= i
        if temp_p > 1:
            factors.append(temp_p)

        return len(factors) == 2

    def eliminate_pairs(self, pairs_to_eliminate):
        self.possible_pairs = [
            pair for pair in self.possible_pairs if pair not in pairs_to_eliminate
        ]

    def does_not_know_numbers(self):
        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            temp_sally = Sally(pair[0] + pair[1])
            temp_sally.initial_elimination()  # Simulate Sally's initial state
            if temp_sally.knows_numbers():
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)
        return not self.knows_numbers()

    def get_numbers(self):
        self.asked += 1
        self.does_not_know_numbers()  # Trigger eliminations
        if self.knows_numbers():  # Check *after* eliminations
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
        self.possible_pairs = [
            pair for pair in self.possible_pairs if pair not in pairs_to_eliminate
        ]

    def initial_elimination(self):
        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            if is_prime(pair[0]) and is_prime(pair[1]):
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)

    def does_not_know_numbers(self):
        pairs_to_eliminate = []
        for pair in self.possible_pairs:
            temp_paul = Paul(pair[0] * pair[1])
            if temp_paul.knows_numbers():
                pairs_to_eliminate.append(pair)
        self.eliminate_pairs(pairs_to_eliminate)
        return not self.knows_numbers()

    def get_numbers(self):
        self.asked += 1
        self.does_not_know_numbers()  # Trigger eliminations
        if self.knows_numbers(): # Check *after* eliminations
            return self.possible_pairs[0]
        else:
            return None


class Tester:
    def __init__(self):
        self.a = random.randint(2, 19)  # Numbers greater than 1
        self.b = random.randint(2, 19)
        self.a = 1
        self.b = 6
        self.P = self.a * self.b
        self.S = self.a + self.b
        self.paul = Paul(self.P)
        self.sally = Sally(self.S)
        print(f"a = {self.a}, b = {self.b}, P = {self.P}, S = {self.S}")

    def run_conversation(self):
        MAX_TURNS = 5
        turn = 0
        while turn < MAX_TURNS:
            turn += 1
            print(f"Turn {turn}:")

            paul_numbers = self.paul.get_numbers()
            if paul_numbers is None:
                print(f"  Paul's possible pairs: {self.paul.possible_pairs}")
            else:
                print(f"  Paul knows the numbers: {paul_numbers}")
                return

            sally_numbers = self.sally.get_numbers()
            if sally_numbers is None:
                print(f"  Sally's possible pairs: {self.sally.possible_pairs}")
            else:
                print("   Sally knows the numbers:", sally_numbers)
                return
                #  if self.paul.get_numbers() is not None:
                    #  print(f"Sally: The numbers are {sally_numbers}")
                    #  return True
                #  else:
                    #  print("Paul and Sally could not determine the numbers.")
                    #  return False

            #  if paul_numbers is not None and sally_numbers is not None:
                #  break  # Both know the numbers (shouldn't happen, but safe to check)

        #  if self.paul.get_numbers() is not None and self.sally.get_numbers() is not None:
            #  print(f"Paul: The numbers are {self.paul.get_numbers()}")
            #  return True

        print("Paul and Sally could not determine the numbers.")
        return False


# Main execution block
tester = Tester()
tester.run_conversation()
