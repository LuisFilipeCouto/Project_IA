# Project_IA

### About the project 
This project involves the development of an autonoumous agent for playing the game Rush Hour <br>
The [agent](student.py) simulates moves and builds a search tree with custom nodes, each storing relevant information about the current game state, and then uses the A* searching algorithm to explore the tree and find the optimal path. Once the path is found, an algorithm is used to convert it into corresponding keys to move the agent <p>
The [A* algorithm](pathfinding.py) is implemented with the following characteristics:
- admissible heuristic that takes into account multiple information about the current game state
- open node list implemented using a min-heap, with a dynamic evaluation function for insertion ordering
- cycle prevention by keeping a dictionary of visited states
- time limit and number of open nodes limit, to prevent extremely long search times as the levels get more complex 

### Detailed description/usage 
Read the project report -> [**report.pdf**](report.pdf)

To install necessary dependencies (assuming you are in the base directory):
```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

To test the program:
```
python3 server.py    # in terminal 1 
python3 viewer.py    # in terminal 2
python3 student.py   # in terminal 3
```
