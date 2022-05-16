import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
SPEED = 10
FOOD_SIZE = 10

# rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
RED = (255, 0, 0)

Point = namedtuple('Point', ['x', 'y'])


class Direction(Enum):
    """
    No need to care about using number or string here
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class SnakeGame:
    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT):
        self.width = w
        self.height = h
        
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        # control speed of game
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT    # when game start, snake moves to the RIGHT defaultly
        # position of head of snake(when game start, head of snake is at the middle of screen(width/2 & height/2))
        self.head = Point(self.width/2, self.height/2)

        # init snake
        self.snake = [self.head, 
                      Point(self.head.x-FOOD_SIZE, self.head.y),        # "x-" means adding FOOD_SIZE coming from the left
                      Point(self.head.x-(FOOD_SIZE*2), self.head.y),    # "x-" means adding FOOD_SIZE coming from the left
                    #   Point(self.head.x-(FOOD_SIZE*3), self.head.y)
                      ]
        
        # init score
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        """
        Without [*FOOD_SIZE], snake may never get the food
        For example: (0, (10-3)//3) * 3 always give an multiple number(bội số)
        Đảm bảo rằng randint trong khoảng (0, ?) luôn chia hết cho FOOD_SIZE
        Nếu ko chia hết thì snake sẽ ko bh ăn được food(do khác x hoặc y)
        """
        x = random.randint(0, (self.width-FOOD_SIZE)//FOOD_SIZE)*FOOD_SIZE
        y = random.randint(0, (self.height-FOOD_SIZE)//FOOD_SIZE)*FOOD_SIZE
        # x = random.randint(0, round((self.width-FOOD_SIZE))/FOOD_SIZE)*FOOD_SIZE
        # y = random.randint(0, round((self.height-FOOD_SIZE))/FOOD_SIZE)*FOOD_SIZE

        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _move(self, direction):
        # get current position of head
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += FOOD_SIZE
        elif direction == Direction.LEFT:
            x -= FOOD_SIZE
        elif direction == Direction.UP:
            y -= FOOD_SIZE
        elif direction == Direction.DOWN:
            y += FOOD_SIZE
        
        # update position of head after direction
        self.head = Point(x, y)

    def is_collision(self):
        # hit boundary
        if self.head.x > self.width - FOOD_SIZE or self.head.x < 0 or self.head.y > self.height - FOOD_SIZE or self.head.y < 0:
            return True
        # hit itself
        if self.head in self.snake[1:]: # head = snake[0]
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            # draw snake outside
            pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, FOOD_SIZE, FOOD_SIZE))    # top(FOOD_SIZE), left(FOOD_SIZE) is dimension
            # draw snake inside
            # pygame.draw.rect(self.display, RED, pygame.Rect(pt.x+FOOD_SIZE//4, pt.y+FOOD_SIZE//4, FOOD_SIZE//2, FOOD_SIZE//2))
        
        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, FOOD_SIZE, FOOD_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        # put text on the display
        self.display.blit(text, [0, 0])
        # update full display surface to screen. without this we don't see the changes
        pygame.display.flip()

    def _play_step(self):
        #1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # avoid the "implosion": if you are going LEFT and then you press the RIGHT key, it counts like a collision
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                # avoid the "implosion": if you are going RIGHT and then you press the LEFT key, it counts like a collision
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                # avoid the "implosion": if you are going UP and then you press the DOWN key, it counts like a collision
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                # avoid the "implosion": if you are going DOWN and then you press the UP key, it counts like a collision
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                            
        #2. move
        self._move(self.direction)  #update the head
        """
        Insert a new head and remove the tail each time it's doesn't eat the food
        """
        self.snake.insert(0, self.head)
        
        #3. check if game over
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score
        
        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()    # remove the tail
        
        #5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        #6. return game over and score
        return game_over, self.score


if __name__ == '__main__':
    game = SnakeGame()
    
    while True:
        game_over, score = game._play_step()
        
        if game_over == True:
            break

    print('Final Score: ', score)
        
    pygame.quit()