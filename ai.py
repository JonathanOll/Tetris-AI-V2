from copy import deepcopy
from random import randint, uniform


def height_difference(m, moving):  # sum of height difference between each pair of column
    
    lst = []
    
    for x in range(len(m[0])):
    
        for y in range(len(m)):
    
            if m[y][x] != 0 and (x, y) not in moving:
    
                lst.append(len(m) - y)
                break
    
        if x >= len(lst):
    
            lst.append(0)
    
    res = 0
    
    for a in range(len(lst) - 1):
    
        res += abs(lst[a] - lst[a+1])
    
    return res


def max_height(m, moving):
    
    res = 0
    
    for y in range(len(m)):
    
        for x in range(len(m[y])):
    
            if m[y][x] != 0 and len(m) - y > res and (x, y) not in moving:
    
                res = len(m) - y
    
    return res


def completed_line(m, moving):
    
    res = 0
    
    for y in range(len(m)):
    
        ok = True
    
        for x in range(len(m[y])):
    
            if m[y][x] == 0 or (x, y) in moving:
    
                ok = False
    
        if ok:
    
            res +=1
    
    return [0, 1, 3, 5, 8][res]


def hole_count(m, moving):

    res = 0

    for x in range(len(m[0])):

        block_encountered = False

        for y in range(len(m)):

            if (x, y) in moving:

                continue

            if m[y][x] != 0:

                block_encountered = True

            elif block_encountered:

                res += 1

    return res


def rotate(piece):

    width, height = len(piece[0]), len(piece)

    new = [[0] * height for a in range(width)]

    for x in range(width):

        for y in range(height):

            new[x][height-y-1] = piece[y][x]

    return new


def place_at_the_lowest(matrix, piece, xx):  # get game's matrix if a piece was placed at the lowest in a certain position

    matrix = deepcopy(matrix)

    done = False

    for yy in range(len(matrix) - len(piece) + 1):

        ok = True

        for y in range(len(piece)):

            for x in range(len(piece[y])):

                if piece[y][x] != 0:

                    if matrix[yy+y][xx+x] != 0:

                        ok = False

        if ok == False:

            yy = yy - 1

            for y in range(len(piece)):

                for x in range(len(piece[y])):

                    if piece[y][x] != 0:

                        matrix[yy+y][xx+x] = piece[y][x]

            done = True
            break
    
    if not done:

        yy = len(matrix) - len(piece)

        for y in range(len(piece)):

            for x in range(len(piece[y])):

                if piece[y][x] != 0:

                    if matrix[yy+y][xx+x] != 0:

                        return -1

                    matrix[yy+y][xx+x] = piece[y][x]

    return matrix


class Network:
    
    functions = [height_difference, max_height, completed_line, hole_count]  # listes des fonctions pour les indicateurs
    
    def __init__(self, weights=None):
        
        if weights == None:
        
            self.weights = [uniform(-1, 1) for a in range(len(Network.functions))]
        
        else:
        
            self.weights = weights
        
        self.fitness = None

    def predict(self, matrix, moving):  # get score from a game's matrix
        
        res = 0
        
        for a in range(len(Network.functions)):
        
            res += Network.functions[a](matrix, moving) * self.weights[a]
        
        return res

    def get_piece(self, moving):  # isolate moving piece
        
        minx = min(moving, key=lambda a: a[0])[0]
        miny = min(moving, key=lambda a: a[1])[1]
        maxx = max(moving, key=lambda a: a[0])[0]
        maxy = max(moving, key=lambda a: a[1])[1]
        
        piece = [[0] * (maxx - minx + 1) for a in range(maxy-miny + 1)]
        
        for x, y in moving:
        
            piece[y-miny][x-minx] = 1

        return piece

    def best_score(self, mat, piece):  # get the max score for a certain piece and matrix
        
        matrix = deepcopy(mat)
        
        max_score = None
        
        for a in range(4):  # on parcoure chaque rotation
        
            for x in range(len(matrix[0]) - len(piece[0]) + 1):  # et on parcoure chaque position
        
                matrice = place_at_the_lowest(matrix, piece, x)
        
                if matrice == -1: continue  # si on ne peut pas placer la pièce à cette position, on n'effectue même pas les tests
        
                score = self.predict(matrice, [])
        
                if max_score is None or score > max_score:  # si le score est supérieur au score maximal actuel, cette action devient l'action priviliégiée
        
                    max_score = score
        
            piece = rotate(piece)  # on fait tourner la piece
        
        return max_score

    def best_move(self, mat, moving):  # pour obtenir la rotation et la position optimales
        
        if moving == []: return 0, 0
        
        matrix = deepcopy(mat)
        
        for x, y in moving:
        
            matrix[y][x] = 0
        
        piece = self.get_piece(moving)  # on recupere la piece

        max_score = None
        max_score_rot = None
        max_score_x = None

        for rotation in range(4):  # on parcoure chaque rotation
        
            for x in range(len(matrix[0]) - len(piece[0]) + 1):  # et on parcoure chaque position
        
                result_matrix = place_at_the_lowest(matrix, piece, x)
        
                if result_matrix == -1: continue  # si on ne peut pas placer la pièce à cette position, on n'effectue même pas les tests
        
                score = self.predict(result_matrix, [])

                if max_score is None or score > max_score:  # si le score est supérieur au score maximal actuel, cette action devient l'action priviliégiée
        
                    max_score = score
                    max_score_rot = rotation
                    max_score_x = x
        
                elif score == max_score:
        
                    if x < max_score_x:
        
                        max_score_x = x
                        max_score_rot = rotation
        
                    elif rotation < max_score_rot:
        
                        max_score_x = x
                        max_score_rot = rotation
        
            piece = rotate(piece)  # on fait tourner la piece
        
        return max_score_x, max_score_rot

    def child(self, agent2, mutation=0.1):  # créer un nouvel agent à partir de deux agents (crossover)
        
        c = Network()
        
        for a in range(len(c.weights)):
        
            if uniform(0, 1) < 0.5:
        
                c.weights[a] = self.weights[a] + uniform(-mutation, mutation)
        
            else:
        
                c.weights[a] = agent2.weights[a] + uniform(-mutation, mutation)
        
        return c

    def info(self):
        
        print("weights:", self.weights)
        print("fitness:", ("Inconnu" if self.fitness is None else self.fitness))




