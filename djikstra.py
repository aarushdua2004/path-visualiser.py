from tkinter import messagebox, Tk
import pygame
import sys

pygame.init()

pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

window_width = 600
window_height = 600

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25
box_width = window_width // columns
box_height = window_height // rows
grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbors()

def draw_text(win, text, pos, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    win.blit(text_surface, pos)

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False
    start_box = None

    while True:
        for event in pygame.event.get():
            # Quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse position
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                # Draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    if not grid[i][j].start and not grid[i][j].target:
                        grid[i][j].wall = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not start_box_set:
                        x, y = pygame.mouse.get_pos()
                        i = x // box_width
                        j = y // box_height
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        start_box_set = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if not target_box_set:
                        x, y = pygame.mouse.get_pos()
                        i = x // box_width
                        j = y // box_height
                        target_box = grid[i][j]
                        target_box.target = True
                        target_box_set = True
            # Start algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            neighbor.queued = True
                            neighbor.prior = current_box
                            queue.append(neighbor)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (30, 30, 30))
                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (199, 110, 0))
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (250, 250, 250))
                if box.target:
                    box.draw(window, (200, 200, 0))

        instructions = [
            "Instructions:",
            "1. Left click to set start",
            "2. Left click and hold to draw walls",
            "3. Right click to set target",
            "4. Press any key to run"
        ]

        for idx, line in enumerate(instructions):
            draw_text(window, line, (10, window_height - (20 * (len(instructions) - idx))))

        pygame.display.flip()

main()
