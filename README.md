A classic minesweeper game written with pygame.
AI will solve the game using knowledges revealed on the board.

Dependencies
------------
The code was run in `Python 3.12.9`, `pygame 2.6.1` and `numpy 2.2.4`. Other
versions might work too.

How to run
----------
Clone the repository and do `python run.py`. If the window is unresponsive
you should use `pythonw` instead (this depends on OS and Python versions).

Game state is stored near `run.py`.

Code organization
-----------------
Each game element handles its visual representation, logic and input responses.
It looks like a reasonable design for such a simple game. 

There is a `Board` class representing the minesweeper game board and several
(quite sketchy) GUI elements in `gui.py`. There is also a `Leaderboard` class
which stores, updates and displays leaderboard. `MinesweeperAI` class covers AI's
move on the board.

The main `Game` class puts it all together.

Credits
-------
The closed tile sprite and font to display mine counts by kenney.nl

Font for GUI is from here https://fonts.google.com/specimen/Orbitron
