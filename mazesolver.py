import cv2
import numpy as np
from collections import deque
import os

# Global variables to store the start and end points
start = None
end = None

def load_and_process_image(image_path):
    """
    Load an image of the maze, detect the borders, and crop to the maze area.
    """
    print("Loading and processing the image...")
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Cannot open/read file: {image_path}. Check the file path and ensure the file exists.")

    # Invert the image: now black will represent walls and white will represent paths
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Find the bounding box of the non-white pixels (the maze area)
    coords = cv2.findNonZero(binary_image)  # Find all non-zero points (i.e., maze walls)
    x, y, w, h = cv2.boundingRect(coords)  # Find the bounding box of those points
    cropped_image = image[y:y+h, x:x+w]  # Crop the original grayscale image

    print(f"Maze detected and cropped: x={x}, y={y}, w={w}, h={h}")

    # Invert the cropped image: black for walls (1), white for paths (0)
    _, binary_cropped = cv2.threshold(cropped_image, 128, 255, cv2.THRESH_BINARY_INV)
    maze_area = binary_cropped // 255

    # Erode the walls slightly to push the path away from the walls
    eroded_maze = cv2.erode(maze_area.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1)

    print("Image processing and cropping complete.")
    return cropped_image, maze_area, eroded_maze, (x, y)

def mouse_callback(event, x, y, flags, param):
    """
    Mouse callback function to select start and end points.
    """
    global start, end, eroded_maze, cropped_image, offset

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse click detected at: ({x}, {y})")
        if start is None:
            start = (y, x)  # OpenCV uses (x, y), but for numpy array, we use (y, x)
            if eroded_maze[start[0], start[1]] == 1:
                print("Start point is on a wall! Please select a valid start point.")
                start = None
            else:
                print(f"Start point selected at: {start}")
        elif end is None:
            end = (y, x)
            if eroded_maze[end[0], end[1]] == 1:
                print("End point is on a wall! Please select a valid end point.")
                end = None
            else:
                print(f"End point selected at: {end}")
                print("Calculating the shortest route, please wait...")
                solve_and_display_path(cropped_image, eroded_maze, start, end)

def bfs_solve_maze(maze, start, end):
    """
    Solves the maze using Breadth-First Search (BFS) to find the shortest path.
    """
    print("Starting BFS to solve the maze...")
    rows, cols = maze.shape

    queue = deque([(start, [start])])
    visited = set([start])

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            print("Path found!")
            return path

        for move in moves:
            next_position = (x + move[0], y + move[1])
            nx, ny = next_position

            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx, ny] == 0 and next_position not in visited:
                    queue.append((next_position, path + [next_position]))
                    visited.add(next_position)

    print("No path found.")
    return None

def draw_path_on_image(image, path):
    """
    Draw the path on the original maze image as a red line and save the result.
    """
    print("Drawing the path on the image...")

    # Convert to color image for better path visualization
    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Draw the path by connecting the points with a red line
    for i in range(len(path) - 1):
        cv2.line(color_image, (path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]), (0, 0, 255), 2)

    # Save the solved maze image
    output_path = 'solved_maze.png'
    cv2.imwrite(output_path, color_image)
    print(f"Path plotted and saved as {output_path}. Opening the image...")

    # Open the image using the default image viewer
    if os.name == 'nt':  # For Windows
        os.startfile(output_path)
    else:  # For macOS and Linux
        os.system(f'open {output_path}')

def solve_and_display_path(cropped_image, eroded_maze, start, end):
    """
    Solve the maze and display the path on the cropped image.
    """
    path = bfs_solve_maze(eroded_maze, start, end)

    if path:
        print("Path found and being drawn on the maze...")
        draw_path_on_image(cropped_image, path)
    else:
        print("No path found.")

if __name__ == "__main__":
    image_path = 'maze.png'  # Replace with your maze image path

    cropped_image, maze_area, eroded_maze, offset = load_and_process_image(image_path)

    if maze_area is None:
        print("Maze borders could not be detected. Exiting.")
    else:
        cv2.imshow('Select Start and End Points', cropped_image)
        cv2.setMouseCallback('Select Start and End Points', mouse_callback)

        print("Please click on the maze to set the start and end points.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
