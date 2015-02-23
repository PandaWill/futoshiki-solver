from time import sleep
from unittest import TestCase


class FutoshikiTest(TestCase):
    def test_applicable_rules(self):
        f = Futoshiki()

        f.rules = [
            ((0, 0), (1, 0)),
            ((1, 1), (1, 2)),
            ((1, 2), (1, 3)),
            ((2, 1), (2, 0)),
            ((2, 4), (2, 3)),
            ((2, 3), (3, 3)),
            ((4, 1), (4, 2)),
        ]

        self.assertEqual([((0, 0), (1, 0))], f.applicable_rules((0, 0)))
        self.assertEqual([((1, 1), (1, 2)), ((1, 2), (1, 3))], f.applicable_rules((1, 2)))
        self.assertEqual([], f.applicable_rules((1, 4)))

    def test_row_elimination(self):
        f = Futoshiki()

        f.solution[0][0] = {2}
        f.update_row_elimination()

        self.assertEqual({1, 3, 4, 5}, f.solution[0][1])
        self.assertEqual({1, 3, 4, 5}, f.solution[0][2])
        self.assertEqual({1, 3, 4, 5}, f.solution[0][3])
        self.assertEqual({1, 3, 4, 5}, f.solution[0][4])

        f.solution[1][1] = {5}
        f.update_row_elimination()

        self.assertEqual({1, 2, 3, 4}, f.solution[1][0])
        self.assertEqual({1, 2, 3, 4}, f.solution[1][2])
        self.assertEqual({1, 2, 3, 4}, f.solution[1][3])
        self.assertEqual({1, 2, 3, 4}, f.solution[1][4])

    def test_col_elimination(self):
        f = Futoshiki()

        f.solution[0][0] = {2}
        f.update_col_elimination()

        self.assertEqual({1, 3, 4, 5}, f.solution[1][0])
        self.assertEqual({1, 3, 4, 5}, f.solution[2][0])
        self.assertEqual({1, 3, 4, 5}, f.solution[3][0])
        self.assertEqual({1, 3, 4, 5}, f.solution[4][0])

        f.solution[1][1] = {5}
        f.update_col_elimination()

        self.assertEqual({1, 2, 3, 4}, f.solution[0][1])
        self.assertEqual({1, 2, 3, 4}, f.solution[2][1])
        self.assertEqual({1, 2, 3, 4}, f.solution[3][1])
        self.assertEqual({1, 2, 3, 4}, f.solution[4][1])

    def test_is_solved(self):
        self.assertTrue(Futoshiki.is_cell_solved({1}))
        self.assertFalse(Futoshiki.is_cell_solved({0}))
        self.assertRaises(ValueError, Futoshiki.is_cell_solved({}))

    def test_update_rule_elimination(self):
        f = Futoshiki()

        f.solution[0][0] = {2, 3, 4}
        f.rules = [
            ((0, 0), (0, 1)),
            ((1, 0), (0, 0)),
        ]

        f.update_rule_elimination()

        self.assertEqual({3, 4, 5}, f.solution[0][1])
        self.assertEqual({1, 2, 3}, f.solution[1][0])

class Futoshiki():
    def __init__(self, dimension=5):
        self.dimension = dimension
        self.solution = [[{x for x in range(1, self.dimension + 1)} for x in range(0, self.dimension)] for x in range(0, self.dimension)]
        self.rules = []

    @staticmethod
    def is_cell_solved(cell):
        if len(cell) == 0:
            raise ValueError #TODO: Fix this
        return len(cell) == 1

    def get_candidates_from_row(self, row_index, ignore_column_index):
        candidates = set()

        for column_index in range(0, self.dimension):
            if column_index == ignore_column_index:
                continue
            candidates.update(self.solution[row_index][column_index])
        return candidates

    def get_candidates_from_column(self, column_index, ignore_row_index):
        candidates = set()

        for row_index in range(0, self.dimension):
            if row_index == ignore_row_index:
                continue
            candidates.update(self.solution[row_index][column_index])
        return candidates

    def update_only_choice(self):
        for row_index in range(0, self.dimension):
            for column_index in range(0, self.dimension):
                unique_row_candidates = self.solution[row_index][column_index].difference(self.get_candidates_from_row(row_index, column_index))

                if len(unique_row_candidates) == 1:
                    self.solution[row_index][column_index] = unique_row_candidates
                elif len(unique_row_candidates) > 1:
                    raise ValueError

                unique_column_candidates = self.solution[row_index][column_index].difference(self.get_candidates_from_column(column_index, row_index))

                if len(unique_column_candidates) == 1:
                    self.solution[row_index][column_index] = unique_column_candidates
                elif len(unique_column_candidates) > 1:
                    raise ValueError


    def update_row_elimination(self):
        for row in self.solution:
            solved = set()
            for col in row:
                if Futoshiki.is_cell_solved(col):
                    solved.update(col)

            for col in row:
                if not Futoshiki.is_cell_solved(col):
                    col.difference_update(solved)

    def update_col_elimination(self):
        for col_index in range(0, self.dimension):
            solved = set()
            for row in self.solution:
                if Futoshiki.is_cell_solved(row[col_index]):
                    solved.update(row[col_index])

            for row in self.solution:
                if not Futoshiki.is_cell_solved(row[col_index]):
                    row[col_index].difference_update(solved)

    def update_rule_elimination(self):
        for less_than, more_than in self.rules:
            lower = self.solution[less_than[0]][less_than[1]]
            upper = self.solution[more_than[0]][more_than[1]]

            lower.difference_update({x for x in range(max(upper), self.dimension + 1)})
            upper.difference_update({x for x in range(1, min(lower) + 1)})

    def applicable_rules(self, index):
        return [(x, y) for x, y in self.rules if x == index or y == index]

    def is_solved(self):
        for row in self.solution:
            for col in row:
                if not Futoshiki.is_cell_solved(col):
                    return False
        return True

    def solve(self, step=False):
        while not self.is_solved():
            self.update_rule_elimination()
            print(self)
            sleep(0.3)
            self.update_col_elimination()
            print(self)
            sleep(0.3)
            self.update_row_elimination()
            print(self)
            sleep(0.3)
            self.update_only_choice()
            print(self)
            sleep(0.3)
        print(self)


    # Horrible mess to output it nicely
    def __str__(self):
        printed_puzzle = " " + " -  " * self.dimension + "\n"

        for row, row_values in enumerate(self.solution):
            printed_puzzle += "| "

            for col, values in enumerate(row_values):
                if Futoshiki.is_cell_solved(values):
                    printed_puzzle += str(next(iter(values)))  #Only print number if solution found
                else:
                    printed_puzzle += " "
                    #printed_puzzle += str(values)

                applicable_rules = self.applicable_rules((row, col))
                if ((row, col), (row, col+1)) in applicable_rules:
                    printed_puzzle += " < "
                elif ((row, col+1), (row, col)) in applicable_rules:
                    printed_puzzle += " > "
                else:
                    printed_puzzle += " | "

            printed_puzzle += "\n "

            # Output our separator row
            for col in range(0, self.dimension):
                applicable_rules = self.applicable_rules((row, col))
                if ((row, col), (row + 1, col)) in applicable_rules:
                    printed_puzzle += " ^  "
                elif ((row+1, col), (row, col)) in applicable_rules:
                    printed_puzzle += r" V  "

                else:
                    printed_puzzle += "--- "

            printed_puzzle += "\n"

        return printed_puzzle


def test_puzzle_one():
    f = Futoshiki()

    f.solution[0][0] = {2}
    f.solution[2][0] = {4}
    f.solution[4][3] = {3}

    f.rules = [
        ((0,0),(1,0)),
        ((1,1),(1,2)),
        ((1,2),(1,3)),
        ((2,1),(2,0)),
        ((2,4),(2,3)),
        ((2,3),(3,3)),
        ((4,1),(4,2)),
    ]

    return f

def test_puzzle_two():
    f = Futoshiki()

    f.solution[1][1] = {2}
    f.solution[3][4] = {5}
    f.solution[4][4] = {2}

    f.rules = [
        ((0,2),(0,1)),
        ((1,1),(1,0)),
        ((1,2),(2,2)),
        ((2,0),(2,1)),
        ((2,3),(1,3)),
        ((3,2),(3,3)),
        ((4,0),(3,0)),
        ((4,1),(3,1)),
    ]

    return f


if __name__ == "__main__":

    f = test_puzzle_two()
    f.solve()
