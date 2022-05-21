import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self, i):
        node = self.frontier[i]
        self.frontier = self.frontier[:i] + self.frontier[i+1:]
        return node

    def removedepth(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    def removebroadth(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.explored = set()
        # self.route = []


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        # print(solution)
        # print(list(enumerate(self.walls)))
        for i, row in enumerate(self.walls):
            # print(list(enumerate(row)))
            for j, col in enumerate(row):
                if col:
                    print("\033[7;37m   \033[0m", end="")
                elif (i, j) == self.start:
                    print("\033[7;33m A \033[0m", end="")
                elif (i, j) == self.goal:
                    print("\033[7;33m B \033[0m", end="")
                elif solution is not None and (i, j) in solution:
                    print("\033[7;33m   \033[0m", end="")
                elif (i, j) in self.explored:
                    print("\033[7;34m   \033[0m", end="")
                else:
                    print("   ", end="")
                    # ███
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("right", (row, col + 1)),
            ("left", (row, col - 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solvedepth(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.removedepth()
            self.num_explored += 1
            # self.route.append(self.explored)

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                # print(self.solution)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def solvebroadth(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.removebroadth()
            self.num_explored += 1
            # self.route.append(self.explored)

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                # print(self.solution)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def solvegreedy(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            min = 0
            num = 0
            length = 999
            for tmp in frontier.frontier:
                x1 = tmp.state[0]
                y1 = tmp.state[1]
                x2 = self.goal[0]
                y2 = self.goal[1]
                l = abs(x2 - x1) + abs(y2 - y1)
                if l <= length:
                    min = num
                    length = l
                num += 1
            node = frontier.remove(min)

            self.num_explored += 1
            # self.route.append(self.explored)

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                # print(self.solution)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def solveAstar(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        count = [0,]

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            min = 0
            num = 0
            length = 999
            for tmp in frontier.frontier:
                x1 = tmp.state[0]
                y1 = tmp.state[1]
                x2 = self.goal[0]
                y2 = self.goal[1]
                l = abs(x2 - x1) + abs(y2 - y1) + count[num]
                if l <= length:
                    min = num
                    length = l
                num += 1
            node = frontier.remove(min)
            way = count[min] + 1
            count = count[:min] + count[min + 1:]

            self.num_explored += 1
            # self.route.append(self.explored)

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                # print(self.solution)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    count.append(way)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


# if len(sys.argv) != 2:
#     sys.exit("Usage: python maze.py maze1.txt")
# sys.argv[1]

m = Maze("maze2.txt")
print("Maze:")
m.print()
print("Solving...")
m.solvedepth()
# m.solvebroadth()
# m.solvegreedy()
# m.solveAstar()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze1.png", show_explored=True)

m = Maze("maze2.txt")
print("Maze:")
m.print()
print("Solving...")
# m.solvedepth()
m.solvebroadth()
# m.solvegreedy()
# m.solveAstar()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze2.png", show_explored=True)

m = Maze("maze2.txt")
print("Maze:")
m.print()
print("Solving...")
# m.solvedepth()
# m.solvebroadth()
m.solvegreedy()
# m.solveAstar()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze3.png", show_explored=True)

m = Maze("maze2.txt")
print("Maze:")
m.print()
print("Solving...")
# m.solvedepth()
# m.solvebroadth()
# m.solvegreedy()
m.solveAstar()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze4.png", show_explored=True)
