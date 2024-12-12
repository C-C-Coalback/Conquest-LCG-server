# Conquest-LCG-server
The Conquest-LCG-server will be a server that handles all games of Conquest currently being played. This includes:

  -Receiving requests to create a game.

  -Processing deck loading.
  
  -Receiving instructions for updating the game.
  
  -Sending the current board-state back to the user(s).
  
  -Closing a game when it is complete.

This does NOT include deckbuilding; this is a process that can be done entirely client side.

Update: might include deckbuilding, will see.

Currently the server can send a string containing the current game state, then the client can render it.
The actual game is not yet working.
