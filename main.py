from PIL import Image
import os
from collections import deque

PNG_DIR = "maze.png"

MAZE_IMAGE = Image.open(PNG_DIR)
WIDTH, HIGHT = MAZE_IMAGE.size

def prepare_maze_array():
    for y in range(WIDTH):
        row = []
        for x in range(HIGHT):
            color = MAZE_IMAGE.getpixel((x, y))
            if color == (255, 255, 255, 255):   #white
                row.append(0)
            if color == (0, 0, 0, 255):         #black
                row.append(1)
            if color == (0, 255, 0, 255):       #green
                row.append(0)
                start = (x, y)
            if color == (255, 0, 0, 255):       #red
                row.append(0)
                end = (x, y)
        maze.append(row)
    return start, end


def generate_img(cords: tuple, color: tuple) -> None:
    new_image = images[len(images) - 1].copy()
    new_image.putpixel(cords, color)
    images.append(new_image)

def solve():
    i = 0

    while len(frontier) != 0:
        current = frontier.pop()

        x = current[0]
        y = current[1]

        if visited[y][x] == True:
            continue

        if maze[y][x - 1] == 0 and visited[y][x - 1] == False:   #left is not wall or visited
            frontier.appendleft((x - 1, y))
            solution[(x - 1, y)] = current

        if maze[y][x + 1] == 0 and visited[y][x + 1] == False:   #right is not wall or visited
            frontier.appendleft((x + 1, y))
            solution[(x + 1, y)] = current

        if maze[y + 1][x] == 0 and visited[y + 1][x] == False:   #up is not wall or visited
            frontier.appendleft((x, y + 1))
            solution[(x, y + 1)] = current

        if maze[y - 1][x] == 0 and visited[y - 1][x] == False:   #down is not wall or visited
            frontier.appendleft((x, y - 1))
            solution[(x, y - 1)] = current

        visited[y][x] = True

        generate_img(current, (0, 0, 255, 255))

        i += 1

    print("Done in {} iterations".format(i))

def backtrack():
    runner = end
    i = 0
    solution_image = MAZE_IMAGE.copy()

    while runner != start:
        solution_image.putpixel(runner, (0, 255, 0, 255))
        runner = solution[runner]
        i += 1

        generate_img(runner, (0, 255, 0, 255))

    
    solution_image = solution_image.resize((1024, 1024), resample=Image.BOX)
    solution_image.save("solution.png")
    print("shortest path: {}".format(i))

if __name__ == "__main__":

    maze = []
    frontier = deque()
    visited = [[False] * WIDTH for _ in range(HIGHT)]
    solution = {}
    images = []

    start, end = prepare_maze_array()

    frontier.appendleft(start)

    images.append(MAZE_IMAGE)
    solve()
    backtrack()

    gif = []
    for idx in range(len(images)):
        if idx%7 == 0:
            resized_image = images[idx].resize((1024, 1024), resample=Image.BOX)
            gif.append(resized_image)

    gif[0].save('result.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0, duration=20)