# mazeSolver

## About

A simple python script that solves a maze stored in a text file. It does so by using
either the breadth- or depth-first search algorithm.

## Prerequisites

In principle, you should only need [Python 3](https://www.python.org/) in order to run
this script. It does not depend on any other packages.

## Disclaimer

This was a simple, few hour project of mine, just for fun, so I cannot guarantee you that
it works absolutely optimally. In fact, it runs 100% in Python, which is known to be notoriously 
slow, and for really huge mazes it can take some time (and memory) to find a solution. But hey, 
why would you even store your huge maze in a dumbly formatted text file anyway?

Also, in this project I try to use a few more-or-less *fancy* Python features, like
- custom exceptions
- the `super` function
- f-strings
- decorators, class- and staticmethods
- type hints
- magic methods, other than the *boring* `__init__`
- CLI parsing
- pickling
- [Sphinx docstrings](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)

Wild, right? For a functionality like this (i.e., maze solving) these are probably dispensable and unnecessary 
overcomplications, but for a good coding exercise these are somewhat requirements IMHO.

## Usage

After downloading the script run it in your terminal:
```bash
python3 main.py
```

which will whine to you that several required arguments are not provided. For example, for a maze solver 
to work correctly, usually you need to provide a maze. You can create your favorite maze in your favorite text
editor or download my example mazes from this repo. These text files can contain the following characters:
- `#` for a maze wall
- ` ` (space) for a traversable cell
- `S` for a start point (can only contain one per maze)
- `E` for an end point (can contain multiple)

Also, at the start of a line you can have `//` if you need to comment out something in your maze. (Don't ask me
why on Earth would you need something like that.) Now that your maze is ready to be solved you can run the script:

```bash
python3 main.py -m awesome_maze.txt -a bfs -o awesome_maze_solved_with
```

which will solve your maze with the breadth-first search (bfs) algorithm and creates an output file with the name
`awesome_maze_solved_with_bfs.txt`. Obviously, if you want to use the depth-first search, type `-a dfs`, or if you
are adventurous and want both, type `-a both`. Last things last, there is a `-sp` flag, which, when used, will 
also save a pickled file of the `Maze` instance for later use. This pickled file is also accepted as an input to
the script (after the `-m` flag).

The solution file is also a text file containing the original text representation of your maze and also `*` characters
representing the path found by the corresponding algorithm.

## License and Contributions

This is a free and open-source scpript, so feel free to modify it as you wish. And if you have some comments or criticism,
I will gladly listen to them.
