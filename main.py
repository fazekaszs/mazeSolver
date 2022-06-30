import os
import pickle
from enum import Enum, unique
from pathlib import Path
from typing import Union, List, Dict, Tuple
from argparse import ArgumentParser


class InvalidMazeChar(Exception):

    def __init__(self, char, position):
        super().__init__(f"Invalid character found in the maze: \"{char}\" at {position}!")


class MultipleStartError(Exception):

    def __init__(self, position):
        super().__init__(f"A second start character found in the maze at {position}! "
                         f"Only one start character is allowed per maze!")


class NoStartError(Exception):

    def __int__(self):
        super().__init__("No start character found in the maze!")


class UnknownExtensionError(Exception):

    def __int__(self, extension):
        super().__init__(f"Unknown file extension for maze: {extension}")


@unique
class CellType(Enum):
    FREE = " "
    WALL = "#"
    START = "S"
    END = "E"

    @classmethod
    def chars_to_ct(cls):
        internal_dict = {member.value: member for member in cls.__members__.values()}
        return internal_dict


class Maze:

    @staticmethod
    def _point_neighbours(point: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [
            (point[0] + 1, point[1]),
            (point[0] - 1, point[1]),
            (point[0], point[1] + 1),
            (point[0], point[1] - 1)
        ]

    def __init__(self, path_to_maze: Union[str, Path]):
        """
        Initializes a Maze instance from a text file. The text file can only contain the
        following characters:
            - ' ' i.e., free square
            - '#' i.e., wall
            - 'S' i.e., a start point
            - 'E' i.e., an end point
        The maze can only contain one start point, but multiple end points.
        Comments are allowed in the maze file with the "//" syntax.

        :param path_to_maze: The path to the maze text file.
        """

        assert os.path.exists(path_to_maze), "Invalid path to the maze!"
        assert os.path.isfile(path_to_maze), "Path to the maze is not a file!"

        with open(path_to_maze, "r") as f:
            raw_maze: str = f.read()

        raw_maze: List[str] = list(filter(lambda x: len(x) != 0 and not x.startswith("//"), raw_maze.split("\n")))

        for line in raw_maze:
            assert len(line) == len(raw_maze[0]), "All lines must have the same length!"

        self.grid_corner: Tuple[int, int] = (len(raw_maze), len(raw_maze[0]))

        chars_to_ct: Dict[str, CellType] = CellType.chars_to_ct()

        self.start_point: Union[None, Tuple[int, int]] = None
        self.grid: Dict[Tuple[int, int], CellType] = {}
        for line_idx, line in enumerate(raw_maze):
            for char_idx, char in enumerate(line):

                try:
                    self.grid[(line_idx, char_idx)] = chars_to_ct[char]
                except KeyError:
                    raise InvalidMazeChar(char, (line_idx, char_idx))

                if chars_to_ct[char] == CellType.START and self.start_point is not None:
                    raise MultipleStartError((line_idx, char_idx))
                elif chars_to_ct[char] == CellType.START:
                    self.start_point = (line_idx, char_idx)

        if self.start_point is None:
            raise NoStartError()

        self.bfs_solution = None
        self.dfs_solution = None

    def __str__(self):

        out = ""
        for row_idx in range(self.grid_corner[0]):
            for col_idx in range(self.grid_corner[1]):
                out += self.grid[(row_idx, col_idx)].value
            out += "\n"
        return out

    def breadth_first_search(self) -> List[Tuple[int, int]]:

        routes: List[List[Tuple[int, int]]] = [[self.start_point, ], ]

        while len(routes) > 0:

            new_routes: List[List[Tuple[int, int]]] = list()
            for route in routes:
                for nb_point in Maze._point_neighbours(route[-1]):

                    if nb_point not in self.grid:
                        continue  # point off the grid

                    if self.grid[nb_point] == CellType.WALL:
                        continue  # point goes into a wall

                    if self.grid[nb_point] == CellType.END:
                        self.bfs_solution = list(route) + [nb_point, ]  # we found the solution
                        return self.bfs_solution

                    if nb_point in route:
                        continue  # point already visited

                    # Point is on the grid, is not a wall, is not the end, and hasn't been visited yet.
                    new_route = list(route) + [nb_point, ]
                    new_routes.append(new_route)

            routes = new_routes

        print("We did not find any solutions for the maze!")

    def depth_first_search(self) -> List[Tuple[int, int]]:

        route: List[Tuple[int, int]] = [self.start_point, ]
        possible_steps: List[List[Tuple[int, int]]] = list()

        while len(route) > 0:

            # Select neighbouring point of the last route point.
            nb_points = Maze._point_neighbours(route[-1])

            # Remove neighbours that are not valid.
            point_to_remove: List[int] = list()
            for idx, nb_point in enumerate(nb_points):

                if nb_point not in self.grid:
                    point_to_remove.append(idx)
                    continue

                if self.grid[nb_point] == CellType.WALL:
                    point_to_remove.append(idx)
                    continue

                if self.grid[nb_point] == CellType.END:
                    self.dfs_solution = route + [nb_point, ]
                    return self.dfs_solution

                if nb_point in route:
                    point_to_remove.append(idx)
                    continue

            for idx in point_to_remove[::-1]:
                nb_points.pop(idx)

            # Case: we have valid neighbours.
            if len(nb_points) > 0:
                route.append(nb_points.pop())
                possible_steps.append(nb_points)

            # Case: we don't have valid neighbours, but we can backtrace.
            elif len(possible_steps) > 0:

                # Backtrace.
                while len(possible_steps[-1]) == 0:
                    possible_steps.pop()
                    route.pop()

                # Case: after backtrace we exhausted all possible steps.
                if len(possible_steps) == 0:
                    break

                # Case: we still have a nonzero set of possible steps.
                route[-1] = possible_steps[-1].pop()

            # Case: we don't have valid neighbours, and we can't backtrace.
            else:
                break

        print("We did not find any solutions for the maze!")

    def view_bfs(self) -> str:

        if self.bfs_solution is None:
            self.breadth_first_search()

        out = ""
        for row_idx in range(self.grid_corner[0]):
            for col_idx in range(self.grid_corner[1]):
                if (row_idx, col_idx) in self.bfs_solution:
                    out += "*"
                else:
                    out += self.grid[(row_idx, col_idx)].value
            out += "\n"

        return out

    def view_dfs(self) -> str:

        if self.dfs_solution is None:
            self.depth_first_search()

        out = ""
        for row_idx in range(self.grid_corner[0]):
            for col_idx in range(self.grid_corner[1]):
                if (row_idx, col_idx) in self.dfs_solution:
                    out += "*"
                else:
                    out += self.grid[(row_idx, col_idx)].value
            out += "\n"

        return out


def main():

    my_parser = ArgumentParser()
    my_parser.add_argument("-m", "--maze_file", required=True, type=Path,
                           help="The path to the file containing the maze")
    my_parser.add_argument("-a", "--algorithm", required=True, type=str, choices=["bfs", "dfs", "both"],
                           help="The algorithm used for solving the maze.")
    my_parser.add_argument("-o", "--output", required=True, type=str,
                           help="The filename prefix of the output.")
    my_parser.add_argument("-sp", "--save_pickle", action="store_true",
                           help="Whether to save the maze in a pickled format.")
    args = my_parser.parse_args()

    if args.maze_file.suffix == ".txt":
        maze: Maze = Maze(args.maze_file)
    elif args.maze_file.suffix == ".pickle":
        with open(args.maze_file, "rb") as f:
            maze: Maze = pickle.load(f)
    else:
        raise UnknownExtensionError(args.maze_file.suffix)

    if args.algorithm == "bfs" or args.algorithm == "both":

        solution = maze.view_bfs()
        with open(f"{args.output}_bfs.txt", "w") as f:
            f.write(solution)

    if args.algorithm == "dfs" or args.algorithm == "both":

        solution = maze.view_dfs()
        with open(f"{args.output}_dfs.txt", "w") as f:
            f.write(solution)

    if args.save_pickle:

        with open(f"{args.output}.pickle", "wb") as f:
            pickle.dump(maze, f)


if __name__ == "__main__":
    main()
