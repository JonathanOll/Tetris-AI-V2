import pygame
from time import time
import sys
from random import randint, choice
import ai
import matplotlib.pyplot as plt
from options import *

selected = -1
games = []
current_gen = 1
results = [0]
max_results = [0]
graph = None

def load_colors():

    for a in ["blue", "cyan", "green", "magenta", "orange", "red", "yellow"]:
        
        img = pygame.image.load("res/blocks/" + a + ".png")
        
        if SIZE != 16:
            img = pygame.transform.scale(img, (SIZE, SIZE))
        
        COLORS.append(img)

def handle_event(event):
    
    global selected

    for e in event:
     
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
     
            pygame.display.quit()
            sys.exit()
        
        elif e.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if pos[0] < COLUMN * SIZE * 10:
                
                selected_x = pos[0] // (SIZE * 10)
                selected_y = pos[1] // (SIZE * 18)

                selected = selected_x + COLUMN * selected_y

            else:

                selected = -1

        elif e.type == pygame.KEYDOWN:

            if selected != -1:

                if e.key == pygame.K_UP:

                    if selected >= COLUMN: selected -= COLUMN
                
                elif e.key == pygame.K_DOWN:

                    if selected < COLUMN * (ROW - 1): selected += COLUMN
                
                elif e.key == pygame.K_LEFT:

                    if selected > 0: selected -= 1
      
                elif e.key == pygame.K_RIGHT:

                    if selected < ROW*COLUMN - 1: selected += 1

                    

def get_networks(games):

    networks = []

    for game in games:

        if game.controller.network is not None:
            
            networks.append(game.controller.network)

    return networks

def next_gen(games):

    net = get_networks(games)

    if len(net) > 0:
        
        globals()["results"].append(sum(n.fitness for n in net) / len(net))

        globals()["max_results"].append(max(n.fitness for n in net))

    net.sort(key=lambda a: - a.fitness)

    net = net[:min(5, len(net))]

    if len(net) < 5:

        for a in range(ROW * COLUMN - len(net)):

            net.append(ai.Network())

    else:

        for a in range(ROW * COLUMN - len(net)):

            net.append(choice(net[:5]).child(choice(net[:5])))
    
    res = []

    while len(res) < ROW * COLUMN:

        if len(net) > 0:
            
            res.append(Game(Controller(net.pop())))

        else:

            res.append(Game(Controller()))
    
    globals()["current_gen"] += 1
    globals()["selected"] = -1
    
    update_graph()
    
    return res

def draw_centered_string(window, x, y , text, size=15):

    font = pygame.font.Font(pygame.font.match_font("calibri"), size)
    img = font.render(str(text), True, (0, 0, 0))
    window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))


def update_graph():

    fig, ax = plt.subplots(1, 1, figsize=(CANVAS_SIZE[0] / 100, CANVAS_SIZE[1] / 100))

    ax.plot(range(len(globals()["max_results"])), globals()["max_results"], color="tab:red", label="max")

    ax.plot(range(len(globals()["results"])), globals()["results"], color="tab:blue", label="average")

    ax.legend()

    # ax.plot(list(range(len(globals()["results"]))), globals()["results"], color="red")

    fig.patch.set_facecolor((INTERFACE_COLOR[0] / 255, INTERFACE_COLOR[1] / 255, INTERFACE_COLOR[2] / 255))
    # ax.set_facecolor((INTERFACE_COLOR[0] / 255, INTERFACE_COLOR[1] / 255, INTERFACE_COLOR[2] / 255))
    ax.set_facecolor((1, 1, 1))

    fig.canvas.draw()

    globals()["graph"] = fig.canvas.get_renderer().tostring_rgb()

def draw_interface(window):

    base_x, base_y = COLUMN * SIZE * 10, 0

    width, height = SCREEN_WIDTH - base_x, SCREEN_HEIGHT - base_y

    center_x, center_y = base_x + width // 2, base_y + height // 2

    pygame.draw.rect(window, INTERFACE_COLOR, pygame.Rect(base_x, base_y, width, height))

    draw_centered_string(window, center_x, 70, "Current generation", FONT_SIZE)

    draw_centered_string(window, center_x, 115, current_gen, FONT_SIZE)

    if graph is not None:
        
        img = pygame.image.fromstring(graph, CANVAS_SIZE, "RGB")

        window.blit(img, (center_x - img.get_width() // 2, 155))

        draw_centered_string(window, center_x, 160, "Performance evolution", FONT_SIZE)
    
    if selected != -1:

        pygame.draw.rect(window, (INTERFACE_COLOR[0] + 20, INTERFACE_COLOR[1] + 20, INTERFACE_COLOR[2] + 20), (center_x - width // 2 + 10, 420, width - 20, 290))

        draw_centered_string(window, center_x, 450, "Score", FONT_SIZE)

        draw_centered_string(window, center_x, 490, games[selected].score, FONT_SIZE)
        
        draw_centered_string(window, center_x, 530, "Completed lines", FONT_SIZE)

        draw_centered_string(window, center_x, 570, games[selected].completed_lines, FONT_SIZE)

    pygame.display.flip()

class Timer:
    def __init__(self):
        
        self.LAST_GRAVITY = time()
        self.LAST_FAST_GRAVITY = time()
        self.LAST_MOVE = time()
        self.LAST_INTERACT = time()
        self.LAST_ROTATE = time()

        self.GRAVITY_DELAY = 0.5 / SPEED
        self.FAST_GRAVITY_DELAY = 0.15 / SPEED
        self.MOVE_DELAY = 0.1 / SPEED
        self.INTERACT_DELAY = 0.5 / SPEED
        self.ROTATE_DELAY = 0.5 / SPEED

    def is_delay_passed(self, name, update=True):

        current_time = time()

        if name == "gravity" and current_time - self.LAST_GRAVITY >= self.GRAVITY_DELAY:
            
            if update : self.LAST_GRAVITY = current_time
            return True
        
        if name == "fast_gravity" and current_time - self.LAST_FAST_GRAVITY >= self.FAST_GRAVITY_DELAY:
            
            if update : self.LAST_FAST_GRAVITY = current_time
            return True

        elif name == "move" and current_time - self.LAST_MOVE >= self.MOVE_DELAY:

            if update : self.LAST_MOVE = current_time
            return True
        
        elif name == "interact" and current_time - self.LAST_INTERACT >= self.INTERACT_DELAY:

            return True

        elif name == "rotate" and current_time - self.LAST_ROTATE >= self.ROTATE_DELAY:

            if update : self.LAST_ROTATE = current_time
            return True

        return False


    def interact(self):
        
        self.LAST_INTERACT = time()

class Controller:
    def __init__(self, network=None):
        
        self.network = network
        self.pointed_x = -1
        self.pointed_rot = -1
        self.game = None

        self.left = False
        self.right = False
        self.up = False
        self.down = False

    
    def update(self):

        # HUMAN'S MOVES

        if self.network is None:

            self.left = pygame.key.get_pressed()[pygame.K_LEFT]
            self.right = pygame.key.get_pressed()[pygame.K_RIGHT]
            self.up = pygame.key.get_pressed()[pygame.K_UP]
            self.down = pygame.key.get_pressed()[pygame.K_DOWN]
        
        # AI'S MOVES

        else:

            if len(self.game.moving) == 0 : return

            current_x = min(self.game.moving, key=lambda a: a[0])[0]

            if self.pointed_rot == -1 or self.pointed_x == -1 or min(self.game.moving, key=lambda a: a[1])[1] <= 3:
                
                self.pointed_x, self.pointed_rot = self.network.best_move(self.game.matrix, self.game.moving)

            if self.pointed_rot > 0:

                self.up = True

                self.pointed_rot -= 1

            else:

                self.up = False

            if current_x > self.pointed_x:
                
                self.left = True
                self.right = False

            elif current_x < self.pointed_x:

                self.left = False                
                self.right = True
            
            else:

                self.left = False
                self.right = False

            if current_x == self.pointed_x and self.pointed_rot == 0:

                self.down = True

            else:

                self.down = False       

    def reset(self):

        self.pointed_rot = -1

        self.pointed_x = -1   
    
class Game:

    PIECES = [
                [ [1, 1],
                  [1, 1] ],
                [ [0, 1, 0],
                  [1, 1, 1] ],
                [ [1, 0],
                  [1, 0],
                  [1, 1] ],
                [ [0, 1],
                  [0, 1],
                  [1, 1] ],
                [ [0, 1, 1],
                  [1, 1, 0] ],
                [ [1, 1, 0],
                  [0, 1, 1] ],
                [ [1], [1], [1], [1]],
            ]

    def __init__(self, controller, size=(10, 18)):

        self.controller = controller
        self.controller.game = self
        self.timer = Timer()

        self.matrix = [[0] * size[0] for a in range(size[1])]
        self.moving = []
        self.running = True

        self.score = 0
        self.completed_lines = 0
    
    def is_pos_valid(self, x, y):

        if x < 0 or y < 0:
            return False
        
        if x >= len(self.matrix[0]) or y >= len(self.matrix):
            return False
        
        return True

    def can_place(self, x, y, piece):

        for yy in range(len(piece)):

            for xx in range(len(piece[yy])):

                if piece[yy][xx] == 1 and (not self.is_pos_valid(x + xx, y + yy) or self.matrix[y + yy][x + xx] != 0):
                    
                    return False
        
        return True
    
    def place(self, x, y, piece, color):

        for yy in range(len(piece)):

            for xx in range(len(piece[yy])):

                if piece[yy][xx] == 1:
                    
                    self.matrix[y + yy][x + xx] = color

                    self.moving.append((x + xx, y + yy))

    def remove_moving(self):
        
        color = self.matrix[self.moving[0][1]][self.moving[0][0]]

        for x, y in self.moving:

            self.matrix[y][x] = 0
        
        return color

    def place_moving(self, color):

        for x, y in self.moving:

            self.matrix[y][x] = color

    def terminate(self):

        self.running = False

        if self.controller.network is not None:

           self.controller.network.fitness = self.score

    def tick(self):

        # CONTROLLER

        self.controller.update()
        
        # GRAVITY

        apply_gravity = self.timer.is_delay_passed("gravity") or (self.controller.down and self.timer.is_delay_passed("fast_gravity"))

        if apply_gravity:

            for x, y in self.moving:

                if not self.is_pos_valid(x, y+1) or (self.matrix[y+1][x] != 0 and (x, y+1) not in self.moving):
                    apply_gravity = False
                    break
            
            if apply_gravity:

                self.timer.interact()

                for pos in range(len(self.moving)):
                    
                    color = self.remove_moving()
                    
                    self.moving[pos] = (self.moving[pos][0], self.moving[pos][1] + 1)

                    self.place_moving(color)
            
            elif self.timer.is_delay_passed("interact"):

                self.moving.clear()
       
        # ROTATION

        apply_rotation = self.timer.is_delay_passed("rotate")

        if apply_rotation and self.controller.up and self.moving != []:

            min_x = min(self.moving, key=lambda a: a[0])[0]
            min_y = min(self.moving, key=lambda a: a[1])[1]
            max_x = max(self.moving, key=lambda a: a[0])[0]
            max_y = max(self.moving, key=lambda a: a[1])[1]

            center_x, center_y = (min_x + max_x) // 2, (min_y + max_y) // 2
            if center_x == 0: center_x = 1

            for x, y in self.moving:  # premiere boucle pour verifier les emplacements disponibles
                
                new_x, new_y = center_x - center_y + y, center_y + center_x - x
                
                if not self.is_pos_valid(new_x, new_y) or (self.matrix[new_y][new_x] != 0 and (new_x, new_y) not in self.moving):
                
                   apply_rotation = False
                   break

            if apply_rotation:

                self.timer.interact()

                color = self.remove_moving()

                for a in range(len(self.moving)):

                    pos = self.moving[a]

                    self.moving[a] = (center_x - center_y + pos[1], center_y + center_x - pos[0])
                
                self.place_moving(color)

        # MOVEMENT

        apply_movement = self.timer.is_delay_passed("move")
        movement = -1 if self.controller.left else 1 if self.controller.right else 0

        if apply_movement and movement != 0:

            for x, y in self.moving:

                if not self.is_pos_valid(x + movement, y) or (self.matrix[y][x + movement] != 0 and (x + movement, y) not in self.moving):
                    
                    apply_movement = False
                    break
            
            if apply_movement:

                self.timer.interact()

                for pos in range(len(self.moving)):

                    color = self.remove_moving()

                    self.moving[pos] = (self.moving[pos][0] + movement, self.moving[pos][1])
        
                    self.place_moving(color)

        # LINES CHECK

        completed_lines_count = 0

        if self.moving == []:

            for y in range(len(self.matrix)):
                
                line_completed = True

                for x in range(len(self.matrix[y])):

                    if self.matrix[y][x] == 0 or (x, y) in self.moving:

                        line_completed = False
                        break
                
                if line_completed:

                    self.matrix.pop(y)
                    completed_lines_count += 1

                    self.matrix.insert(0, [0] * len(self.matrix[0]))

        self.score += [0, 100, 300, 500, 800][completed_lines_count]
        self.completed_lines += completed_lines_count

        # SPAWN PIECE IF NEEDED

        if self.moving == []:

            piece = choice(Game.PIECES)

            if self.can_place(len(self.matrix[0]) // 2 - len(piece[0]) // 2, 0, piece):

                self.place(len(self.matrix[0]) // 2 - len(piece[0]) // 2, 0, piece, randint(1, len(COLORS) - 1))

            else:

                self.terminate()
        
            self.controller.reset()

    def paint(self, screen, x_base, y_base, background_diff, infos=False):
        
        background_color = (15 + background_diff, 15 + background_diff, 15 + background_diff) if self.running else (150 + background_diff, 15 + background_diff, 15 + background_diff)

        pygame.draw.rect(screen, background_color, pygame.Rect(x_base, y_base, len(self.matrix[0]) * SIZE, len(self.matrix) * SIZE))
        
        for y in range(len(self.matrix)):
        
            for x in range(len(self.matrix[y])):
        
                if self.matrix[y][x] != 0:
        
                    screen.blit(COLORS[self.matrix[y][x]-1], (x_base + x * SIZE, y_base + y * SIZE))
        
        pygame.display.flip()

    def run(self):
        while True:
            self.tick()

if __name__ == "__main__":

    load_colors()
    update_graph()

    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris AI")
    pygame.display.set_icon(pygame.image.load("res/blocks/red.png"))

    for a in range(ROW*COLUMN):
        
        games.append(Game(Controller(ai.Network())))

    while True:

        handle_event(pygame.event.get())

        running = False

        for a in range(len(games)):
            
            game = games[a]

            if game.running:
                
                running = True
                
                game.tick()
                game.paint(window, a*10*SIZE % (COLUMN * 10 * SIZE), a // COLUMN * 18 * SIZE, 10 * ((a // COLUMN + a) % 2) + (50 if selected == a else 0))

        if not running:
            
            games = next_gen(games)

        draw_interface(window)