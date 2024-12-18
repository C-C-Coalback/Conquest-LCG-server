# Conquest-LCG-server
The Conquest-LCG-server will be a server that handles all games of Conquest currently being played. This includes:

  -Receiving requests to create a game. (COMPLETE!)

  -Processing deck loading. (COMPLETE! though clients can send illegitimate decks. but they are quite funny so for now it can stay.)
  
  -Receiving instructions for updating the game. (COMPLETE!)

  -Actually updating the game. (Partially complete, under active development.)
  
  -Sending the current board-state back to the users. (Mostly complete, cards in victory display are not sent. Also currently both players hands are shown, even though really each player should only be shown their own hand.)
  
  -Closing a game when it is complete.

Currently the server can send the game to the client and accept positions clicked on by the client. It is also capable of handling the deploy phase, though only the very basic functions, such as playing a support to the HQ, or playing an army unit to a planet. No card specific interactions implemented.

The command phase has now also been implemented.
