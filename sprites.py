import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path

class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        print("Agent Aki")
        path = [game_map[self.row][self.col]]
        visited = [[False for i in range(len(game_map[0]))] for i in range(len(game_map))]
        pos = [self.row, self.col]
        stack = []
        path = []
        stack.append(pos)
        

        while(len(stack) != 0):
            pos = stack.pop()

            visited[pos[0]][pos[1]] = True
            path.append(game_map[pos[0]][pos[1]])
            if goal[0] == pos[0] and goal[1] == pos[1]:
                break
            
            
            next = []
            cost = 5000
            
            if pos[0] > 0 and visited[pos[0] - 1][pos[1]] == False and cost > game_map[pos[0] - 1][pos[1]].cost():
                next = [pos[0] - 1, pos[1]]
                cost = game_map[next[0]][next[1]].cost()
                stack.append(next)

            if pos[1] < len(game_map[0]) - 1 and visited[pos[0]][pos[1] + 1] == False and cost > game_map[pos[0]][pos[1] + 1].cost():
                next = [pos[0], pos[1] + 1]
                cost = game_map[next[0]][next[1]].cost()
                stack.append(next)

            if pos[0] < len(game_map) - 1 and visited[pos[0] + 1][pos[1]] == False and cost > game_map[pos[0] + 1][pos[1]].cost():
                next = [pos[0] + 1, pos[1]]
                cost = game_map[next[0]][next[1]].cost()
                stack.append(next)

            if pos[1] > 0 and visited[pos[0]][pos[1] - 1] == False and cost > game_map[pos[0]][pos[1] - 1].cost():
                next = [pos[0], pos[1] - 1]
                cost = game_map[next[0]][next[1]].cost()
                stack.append(next)
            
            

            if cost == 5000: # Player stuck => backtrack
                if len(path) > 1:
                    path.pop()
                    tile = path.pop()
                    stack.append([tile.row, tile.col])
            
            
            #print(stack)
            #print(len(path))

        return path

class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def calcCost(game_map, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(game_map) or pos[1] >= len(game_map[0]):
            return 5000
        
        cost = 0
        num = 0

        if pos[0] > 0:
            cost = cost + game_map[pos[0] - 1][pos[1]].cost()
            num = num + 1
        if pos[0] < len(game_map) - 1:
            cost = cost + game_map[pos[0] + 1][pos[1]].cost()
            num = num + 1
        if pos[1] > 0:
            cost = cost + game_map[pos[0]][pos[1] - 1].cost()
            num = num + 1
        if pos[1] < len(game_map[0]) - 1:
            cost = cost + game_map[pos[0]][pos[1] +1].cost()
            num = num + 1
        
        if num == 0:
            cost = 5000
        
        return cost/num

    def get_agent_path(self, game_map, goal):
        path = []
        discovered = [[False for i in range(len(game_map[0]))] for i in range(len(game_map))]
        discovered[self.row][self.col] = True
        pred = [[[] for i in range(len(game_map[0]))] for i in range(len(game_map))]
        pred[self.row][self.col] = [[], 0]
        pos = [self.row, self.col]
        queue = []
        queue.append(pos)
        
        while(len(queue) > 0):
            pos = queue.pop(0)
            print(pos)

            if pos[0] == goal[0] and pos[1] == goal[1]:
                # print('nasao')
                break

            tiles = []
            if pos[0] > 0 and discovered[pos[0] - 1][pos[1]] == False:
                next = [pos[0] - 1, pos[1]]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[pos[0] - 1][pos[1]] = True
                tiles.append([next, Jocke.calcCost(game_map, next)])
            if pos[1] < len(game_map[0]) - 1 and discovered[pos[0]][pos[1] + 1] == False:
                next = [pos[0], pos[1] + 1]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[pos[0]][pos[1] + 1] = True
                tiles.append([next, Jocke.calcCost(game_map, next)])
            if pos[0] < len(game_map) - 1 and discovered[pos[0] + 1][pos[1]] == False:
                next = [pos[0] + 1, pos[1]]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[pos[0] + 1][pos[1]] = True
                tiles.append([next, Jocke.calcCost(game_map, next)])
            if pos[1] > 0 and discovered[pos[0]][pos[1] - 1] == False:
                next = [pos[0], pos[1] - 1]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[pos[0]][pos[1] - 1] = True
                tiles.append([next, Jocke.calcCost(game_map, next)])
            tiles.sort(key=lambda tile: tile[1])

            for t in tiles:
                queue.append(t[0])
     
        next = goal
        while next != [self.row, self.col]:
            path.append(game_map[next[0]][next[1]])
            next = pred[next[0]][next[1]]

        path.append(game_map[self.row][self.col])
        path.reverse()
        return path

class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        discovered = [[False for i in range(len(game_map[0]))] for i in range(len(game_map))]
        discovered[self.row][self.col] = True
        pred = [[[] for i in range(len(game_map[0]))] for i in range(len(game_map))]
        pred[self.row][self.col] = [[], 0]
        pos = [self.row, self.col]
        queue = []
        queue.append([pos, 0, 0])
        
        while(len(queue) > 0):
            tile = queue.pop(0)
            pos = tile[0]
            cost = tile[1]
            lenght = tile[2]
            # print(pos)

            if pos[0] == goal[0] and pos[1] == goal[1]: # pronasao
                break

            if pos[0] > 0 and discovered[pos[0] - 1][pos[1]] == False:
                next = [pos[0] - 1, pos[1]]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[next[0]][next[1]] = True
                queue.append([next, cost + game_map[next[0]][next[1]].cost(), lenght + 1])
            if pos[1] < len(game_map[0]) - 1 and discovered[pos[0]][pos[1] + 1] == False:
                next = [pos[0], pos[1] + 1]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[next[0]][next[1]] = True
                queue.append([next, cost + game_map[next[0]][next[1]].cost(), lenght + 1])
            if pos[0] < len(game_map) - 1 and discovered[pos[0] + 1][pos[1]] == False:
                next = [pos[0] + 1, pos[1]]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[next[0]][next[1]] = True
                queue.append([next, cost + game_map[next[0]][next[1]].cost(), lenght + 1])
            if pos[1] > 0 and discovered[pos[0]][pos[1] - 1] == False:
                next = [pos[0], pos[1] - 1]
                pred[next[0]][next[1]] = [pos[0], pos[1]]
                discovered[next[0]][next[1]] = True
                queue.append([next, cost + game_map[next[0]][next[1]].cost(), lenght + 1])
            
            queue.sort(key=lambda tile: tile[2])
            queue.sort(key=lambda tile: tile[1])

     
        next = goal
        while next != [self.row, self.col]:
            path.append(game_map[next[0]][next[1]])
            next = pred[next[0]][next[1]]

        path.append(game_map[self.row][self.col])
        path.reverse()
        print(discovered)
        return path

class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        discovered = [[False for i in range(len(game_map[0]))] for i in range(len(game_map))]
        discovered[self.row][self.col] = True
        pred = [[[] for i in range(len(game_map[0]))] for i in range(len(game_map))]
        pred[self.row][self.col] = [[], [], 0]
        pos = [self.row, self.col]
        queue = []
        queue.append([pos, 0, 0])
        
        while(len(queue) > 0):
            tile = queue.pop(0)
            pos = tile[0]
            cost = tile[1]
            # print(pos)

            if pos[0] == goal[0] and pos[1] == goal[1]: # pronasao
                break

            h = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

            if pos[0] > 0:
                next = [pos[0] - 1, pos[1]]
                nextCost = cost + game_map[next[0]][next[1]].cost()
                if discovered[next[0]][next[1]] == False or pred[next[0]][next[1]][2] > nextCost:
                    pred[next[0]][next[1]] = [pos[0], pos[1], nextCost]
                    discovered[next[0]][next[1]] = True
                    queue.append([next, nextCost, h])
            if pos[1] < len(game_map[0]) - 1 and discovered[pos[0]][pos[1] + 1] == False:
                next = [pos[0], pos[1] + 1]
                nextCost = cost + game_map[next[0]][next[1]].cost()
                if discovered[next[0]][next[1]] == False or pred[next[0]][next[1]][2] > nextCost:
                    pred[next[0]][next[1]] = [pos[0], pos[1], nextCost]
                    discovered[next[0]][next[1]] = True
                    queue.append([next, nextCost, h])
            if pos[0] < len(game_map) - 1 and discovered[pos[0] + 1][pos[1]] == False:
                next = [pos[0] + 1, pos[1]]
                nextCost = cost + game_map[next[0]][next[1]].cost()
                if discovered[next[0]][next[1]] == False or pred[next[0]][next[1]][2] > nextCost:
                    pred[next[0]][next[1]] = [pos[0], pos[1], nextCost]
                    discovered[next[0]][next[1]] = True
                    queue.append([next, nextCost, h])
            if pos[1] > 0 and discovered[pos[0]][pos[1] - 1] == False:
                next = [pos[0], pos[1] - 1]
                nextCost = cost + game_map[next[0]][next[1]].cost()
                if discovered[next[0]][next[1]] == False or pred[next[0]][next[1]][2] > nextCost:
                    pred[next[0]][next[1]] = [pos[0], pos[1], nextCost]
                    discovered[next[0]][next[1]] = True
                    queue.append([next, nextCost, h])
            
            queue.sort(key=lambda tile: tile[1] + tile[2])

     
        next = goal
        while next != [self.row, self.col]:
            path.append(game_map[next[0]][next[1]])
            next = [pred[next[0]][next[1]][0], pred[next[0]][next[1]][1]]

        path.append(game_map[self.row][self.col])
        path.reverse()
        print(discovered)
        return path

class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
