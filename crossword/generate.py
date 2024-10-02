import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):

        for variable in self.crossword.variables:
            iterset = self.domains[variable].copy()
            for value in iterset:
                if variable.length == len(value):
                    continue
                self.domains[variable].remove(value)

        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError

    def revise(self, x, y):

        revised = False
        if x in self.crossword.neighbors(y):
            iterset_x = self.domains[x].copy()
            iterset_y = self.domains[y].copy()
            for value_x in iterset_x:
                k = 0
                for value_y in iterset_y:
                    if value_x in self.domains[x] and value_x != value_y and value_x[self.crossword.overlaps[x, y][0]] == value_y[self.crossword.overlaps[x, y][1]]:
                        k += 1
                if k == 0:
                    self.domains[x].remove(value_x)
                    revised = True
        return revised

        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError

    def ac3(self, arcs=None):

        queue = []
        if arcs == None:
            for var in self.crossword.variables:
                for v in self.crossword.neighbors(var):
                    queue.append((var, v))
        elif arcs != None:
            for var in arcs:
                queue.append(var)
        while len(queue) > 0:
            for data in queue:
                if self.revise(data[0], data[1]):
                    if len(self.domains[data[0]]) == 0:
                        return False
                    for value in self.crossword.neighbors(data[0]):
                        if value != data[1]:
                            queue.append((value, data[0]))
                queue.remove(data)
        return True

        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError

    def assignment_complete(self, assignment):

        result = []
        for var in self.crossword.variables:
            if var in assignment.keys():
                result.append(var)
        if len(self.crossword.variables) == len(result):
            return True
        return False

        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError

    def consistent(self, assignment):

        result = []
        for value in assignment.values():
            if list(assignment.values()).count(value) == 1:
                result.append(True)
            else:
                result.append(False)
        for var in assignment.keys():
            if var.length == len(assignment[var]):
                result.append(True)
            else:
                result.append(False)
        for var in assignment.keys():
            for v in self.crossword.neighbors(var):
                if v in assignment.keys():
                    if assignment[var][self.crossword.overlaps[var, v][0]] == assignment[v][self.crossword.overlaps[var, v][1]]:
                        result.append(True)
                    else:
                        result.append(False)
                else:
                    result.append(True)
        if False not in result:
            return True
        else:
            return False

        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):

        values_dict = {}
        for value in self.domains[var]:
            values_dict[value] = 0
        for v in self.crossword.neighbors(var):
            if v not in assignment.keys():
                for value in self.domains[var]:
                    for word in self.domains[v]:
                        if value[self.crossword.overlaps[var, v][0]] == word[self.crossword.overlaps[var, v][1]]:
                            values_dict[value] += 1
        return sorted(list(values_dict.keys()), key=lambda key: values_dict[key])

        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):

        vars = {}
        for var in self.crossword.variables:
            if var not in assignment.keys():
                vars[var] = len(self.domains[var])
        vars = sorted(list(vars.keys()), key=lambda key: vars[key])
        if len(vars) > 1:
            for i in range(len(vars) - 1):
                if vars[i] == vars[i + 1]:
                    n1 = len(self.crossword.neighbors(vars[i]))
                    n2 = len(self.crossword.neighbors(vars[i + 1]))
                    if n1 > n2:
                        return vars[i]
                    elif n2 > n1:
                        return vars[i + 1]
                    else:
                        return vars[i]
        return vars[0]

        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError

    def backtrack(self, assignment):

        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment.pop(var)
        return None

        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
