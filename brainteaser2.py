"""
this code is intended to model this brainteaser:
There are two people, Paul and Sally, both very smart logicians. Paul knows the
product of two natural numbers, greater than zero. He doesn't know the two
natural numbers, just their product. Sally knows the sum of the same two
natural numbers. She doesn't know the natural numbers, just their sum. Paul knows
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

    def find_possible_pairs(self):
        # Initial factor pairs for P, with numbers > 1
        for i in range(2, int(self.P**0.5) + 1):
            if self.P % i == 0:
                self.possible_pairs.append(tuple(sorted((i, self.P // i))))
        if int(self.P**0.5)**2 == self.P and int(self.P**0.5) > 1:
            self.possible_pairs.append(tuple(sorted((int(self.P**0.5), int(self.P**0.5)))))
        self.possible_pairs = sorted(list(set(self.possible_pairs))) # Remove duplicates and sort

    def knows_numbers(self):
        return len(self.possible_pairs) == 1

    def eliminate_based_on_sally_does_not_know(self):
        """Paul eliminates pairs (a, b) if the sum a + b would allow Sally to know initially."""
        pairs_to_eliminate = []
        for a, b in self.possible_pairs:
            temp_sally = Sally(a + b)
            if temp_sally.knows_numbers():
                pairs_to_eliminate.append((a, b))
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]

    def eliminate_based_on_sally_still_does_not_know(self, sally_possible_sums):
        """Paul eliminates pairs (a, b) if the sum a + b is not in Sally's possible sums after her first deduction."""
        pairs_to_eliminate = []
        for a, b in self.possible_pairs:
            if a + b not in sally_possible_sums:
                pairs_to_eliminate.append((a, b))
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]

class Sally:
    def __init__(self, S):
        self.S = S
        self.possible_pairs = []  # List of (a, b) tuples
        self.find_possible_pairs()
        self.initial_elimination()

    def find_possible_pairs(self):
        # Initial pairs that sum to S, with numbers > 1
        for i in range(2, self.S // 2 + 1):
            self.possible_pairs.append(tuple(sorted((i, self.S - i))))
        if self.S % 2 == 0 and self.S // 2 > 1:
            self.possible_pairs.append(tuple(sorted((self.S // 2, self.S // 2))))
        self.possible_pairs = sorted(list(set(self.possible_pairs))) # Remove duplicates and sort

    def knows_numbers(self):
        return len(self.possible_pairs) == 1

    def initial_elimination(self):
        """Sally eliminates sums that can be formed by two primes."""
        pairs_to_eliminate = []
        for a, b in self.possible_pairs:
            if is_prime(a) and is_prime(b):
                pairs_to_eliminate.append((a, b))
        self.eliminate_pairs(pairs_to_eliminate)

    def eliminate_based_on_paul_does_not_know(self):
        """Sally eliminates pairs (a, b) if the product a * b would allow Paul to know initially."""
        pairs_to_eliminate = []
        for a, b in self.possible_pairs:
            temp_paul = Paul(a * b)
            if temp_paul.knows_numbers():
                pairs_to_eliminate.append((a, b))
        self.eliminate_pairs(pairs_to_eliminate)

    def eliminate_based_on_paul_still_does_not_know(self, paul_possible_products):
        """Sally eliminates pairs (a, b) if the product a * b is not in Paul's possible products after his first deduction."""
        pairs_to_eliminate = []
        for a, b in self.possible_pairs:
            if a * b not in paul_possible_products:
                pairs_to_eliminate.append((a, b))
        self.eliminate_pairs(pairs_to_eliminate)

    def eliminate_pairs(self, pairs_to_eliminate):
        self.possible_pairs = [pair for pair in self.possible_pairs if pair not in pairs_to_eliminate]


class Tester:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.P = self.a * self.b
        self.S = self.a + self.b
        self.paul = Paul(self.P)
        self.sally = Sally(self.S)
        print(f"Initial a = {self.a}, b = {self.b}, P = {self.P}, S = {self.S}")
        print(f"Initial Paul's possible pairs: {self.paul.possible_pairs}")
        print(f"Initial Sally's possible pairs: {self.sally.possible_pairs}")

    def run_conversation(self):
        print("\n--- Conversation ---")

        # Turn 1: Paul says "I don't know what the two numbers are."
        if self.paul.knows_numbers():
            print("Error: Paul knew the numbers initially.")
            return

        # Turn 2: Sally says "I don't know what the two numbers are either."
        self.sally.eliminate_based_on_paul_does_not_know()
        if self.sally.knows_numbers():
            print("Error: Sally knew the numbers after Paul's first statement.")
            return
        print("\nAfter Sally's first statement:")
        print(f"  Sally's possible pairs: {self.sally.possible_pairs}")

        # Turn 3: Paul says "I still don't know what the two numbers are."
        paul_initial_possible_products = {a * b for a, b in Paul(self.P).possible_pairs}
        self.paul.eliminate_based_on_sally_does_not_know()
        if self.paul.knows_numbers():
            print("Error: Paul knew the numbers after Sally's first statement.")
            return
        print("\nAfter Paul's second statement:")
        print(f"  Paul's possible pairs: {self.paul.possible_pairs}")

        # Turn 4: Sally says "I still don't know what they are either."
        sally_possible_sums_after_first = {a + b for a, b in Sally(self.S).possible_pairs}
        self.sally.eliminate_based_on_paul_still_does_not_know({a * b for a, b in self.paul.possible_pairs})
        if self.sally.knows_numbers():
            print("Error: Sally knew the numbers after Paul's second statement.")
            return
        print("\nAfter Sally's second statement:")
        print(f"  Sally's possible pairs: {self.sally.possible_pairs}")

        # Turn 5: Paul says "Now I know what the two numbers are."
        self.paul.eliminate_based_on_sally_still_does_not_know({a + b for a, b in self.sally.possible_pairs})
        if self.paul.knows_numbers():
            print("\nPaul now knows the numbers:", self.paul.possible_pairs[0])
            return
        else:
            print("\nError: Paul still doesn't know the numbers.")
            print(f"  Paul's possible pairs: {self.paul.possible_pairs}")


# Main execution block
# We need to test with the correct answer: a=4, b=13
tester = Tester(4, 13)
tester.run_conversation()
