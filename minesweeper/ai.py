import numpy
import random
import json

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __contains__(self, other):
        return self.cells.issuperset(other.cells)
    
    def __sub__(self, other):
        return Sentence(self.cells.difference(other.cells), self.count - other.count) 

    def isempty(self):
        return len(self.cells) == 0

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if not self.isempty() and len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, state_file_path):
        try:
            with open(state_file_path) as state_file:
                state = json.load(state_file)
        except (IOError, json.JSONDecodeError):
            state = {}

        # Load initial height and width
        self.height = state.get('n_rows', 10)
        self.width = state.get('n_cols', 10)
        self.total_mines = state.get('n_mines', 10)

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # Keep the last opened cell's location
        self.last_move = None

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        print(f"Marking {cell} as mine")
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        print(f"Marking {cell} as safe")
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print(f"Opened new cell - {cell}, count: {count}")
        # 1 
        self.moves_made.add(cell)
        self.last_move = cell
        # 2 
        self.mark_safe(cell)

        # 3
        # get neighbour cells 
        neighbours = set()
        x, y = cell
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                # exclude the cell itself
                if (i, j) == cell:
                    continue
                # if cells are already safe, do not add
                if (i, j) in self.safes:
                    continue
                # if cells are already mine, reduce count by 1, and do not add
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # add cells only if they are NOT out of bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        new_sentence = Sentence(neighbours, count)
        print(f"New knowledge got: {new_sentence}")
        self.knowledge.append(new_sentence)

        # 4, 5
        # Iteratively mark guaranteed safes and mines, and infer new knowledge from KB
        # until there isn't newly inferred knowledge
        Changed = True
        depth = 0
        while Changed:
            print(f"Iteration # {depth}")
            depth += 1
            Changed = False

            # update mines or cells with the new sentence
            safes = set()
            mines = set()
            for s in self.knowledge:
                # print(f"known safes for {s}")
                safes.update(s.known_safes())
                mines.update(s.known_mines())
            
            if safes:
                # print(f"safe cells updated: {safes}")
                Changed = True
                for safe in safes:
                    self.mark_safe(safe)

            if mines:
                # print(f"mine cells updated: {mines}")
                Changed = True
                for mine in mines:
                    self.mark_mine(mine)
            
            if not (safes or mines):
                print("No update on safes or mines")

            # remove empty sentences in KB
            self.knowledge = [s for s in self.knowledge if not s.isempty()]
            
            # infer new knowledge by finding subset realation between sentences
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    # print(f"Comparing 2 sentences..\ns1: {s1}\ns2: {s2}")
                    # continue if two are equal sentences
                    if s1 == s2:
                        continue
                    if s1 in s2:
                        # print(f"subset found: {s1} < {s2}")
                        new_sentence = s2 - s1
                        
                        if new_sentence not in self.knowledge:
                            Changed = True
                            print(f"Inferred new sentence: {new_sentence}")
                            self.knowledge.append(new_sentence)