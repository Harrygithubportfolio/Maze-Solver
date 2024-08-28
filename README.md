# Maze Solver

This project is a Python-based Maze Solver that uses image processing and the Breadth-First Search (BFS) algorithm to find the shortest path through a maze. The maze is input as an image, and the program processes the maze to identify paths and walls. The path is then calculated and drawn onto the maze image in red, providing a visual solution to the maze.

## Features

- **Image Processing**: Automatically detects and crops the maze from the input image.
- **Breadth-First Search (BFS)**: Finds the shortest path from the start point to the end point within the maze.
- **Visual Output**: Draws the solution path on the maze image in red and saves the result as an image file.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maze-solver.git
   cd maze-solver
