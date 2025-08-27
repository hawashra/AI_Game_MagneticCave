# AI Game Magnetic-Cave
The magnetic cave is a two-player game similar to Connect 4, except the player must place 5 consecutive pieces to win (in a row, column, or diagonal). The valid moves are in the first or last column (any row) or next to a piece of any color.

## Algorithm used
The min-max algorithm was used in this game.

## The cost function
The cost function for making a move takes in consideration the number of consecuitive pieces for the opponent, as well as for the player himself. Where the AI tries to play in a way that prevents his opponent from making 5 consecuitive pieces, and tries to maximize his opportunities.  

## How to play the game 

```python3 ai_with_ui.py```

Enter the mode (0 for two players, 1 for Player vs AI, 2 for AI vs Player).

Enter the depth if the mode is 1 or 2. It's recommended to use a depth of 1 to 5 for fast responses from the AI.

Click on a square to place a move. 
