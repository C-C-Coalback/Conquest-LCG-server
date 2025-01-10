# Important
I am trying to get a website working first before I do the rest of this. This is proving incredibly difficult.
The repo for the website will be private until I am comfortable with releasing it.

# Conquest-LCG-server
The Conquest-LCG-server will be a server that handles all games of Conquest currently being played. This includes:

  -Receiving requests to create a game. (COMPLETE!)

  -Processing deck loading. (COMPLETE! though clients can send illegitimate decks. but they are quite funny so for now it can stay.)
  
  -Receiving instructions for updating the game. (COMPLETE!)

  -Actually updating the game. (Partially complete, under active development.)
  
  -Sending the current board-state back to the users. (Mostly complete, currently both players hands are shown, even though really each player should only be shown their own hand.)
  
  -Closing a game when it is complete.

Update: Well, that was fast. The core mechanics are (once again) implemented. No card specific effects are here yet (Although I might have copied some over from the original repo and just forgotten). Since this means that the game can be played online, I am calling this version 0.5. Very happy with it.

On the to-do list: There need to be standardised functions when the program is waiting for a particular input, such as a card in a hand, a card in play, etc etc. Currentlz, due to the fairly large size of this code, it is bloating files greatly.
