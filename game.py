import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_W, GRID_H = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

# Colors
BLACK, WHITE, GREEN, RED, YELLOW = (0,0,0), (255,255,255), (0,255,0), (255,0,0), (255,255,0)

# Directions
DIRS = {'UP': (0,-1), 'DOWN': (0,1), 'LEFT': (-1,0), 'RIGHT': (1,0)}

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Game states
        self.levels = {'Slow': 5, 'Fast': 12}
        self.level = None
        self.snake = [(GRID_W//2, GRID_H//2)]
        self.direction = DIRS['RIGHT']
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.menu = True
        
    def new_food(self):
        while True:
            pos = (random.randint(0, GRID_W-1), random.randint(0, GRID_H-1))
            if pos not in self.snake:
                return pos
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.menu:
                    if event.key == pygame.K_1:
                        self.level = 'Slow'
                        self.menu = False
                        self.reset_game()
                    elif event.key == pygame.K_2:
                        self.level = 'Fast'
                        self.menu = False
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                elif self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.menu = True
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP and self.direction != DIRS['DOWN']:
                        self.direction = DIRS['UP']
                    elif event.key == pygame.K_DOWN and self.direction != DIRS['UP']:
                        self.direction = DIRS['DOWN']
                    elif event.key == pygame.K_LEFT and self.direction != DIRS['RIGHT']:
                        self.direction = DIRS['LEFT']
                    elif event.key == pygame.K_RIGHT and self.direction != DIRS['LEFT']:
                        self.direction = DIRS['RIGHT']
                    elif event.key == pygame.K_ESCAPE:
                        self.menu = True
        return True
    
    def reset_game(self):
        self.snake = [(GRID_W//2, GRID_H//2)]
        self.direction = DIRS['RIGHT']
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
    
    def update(self):
        if self.game_over or self.menu:
            return
            
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.new_food()
        else:
            self.snake.pop()
        
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_W or 
            new_head[1] < 0 or new_head[1] >= GRID_H or 
            new_head in self.snake[1:]):
            self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.menu:
            # Menu screen
            title = self.font.render("SNAKE GAME", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - 80, HEIGHT//2 - 60))
            
            slow_text = self.font.render("1 - Slow (Easy)", True, GREEN)
            fast_text = self.font.render("2 - Fast (Hard)", True, RED)
            self.screen.blit(slow_text, (WIDTH//2 - 80, HEIGHT//2))
            self.screen.blit(fast_text, (WIDTH//2 - 80, HEIGHT//2 + 40))
            
        elif self.game_over:
            # Game over screen
            game_over = self.font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            restart = self.font.render("SPACE - Menu", True, YELLOW)
            
            self.screen.blit(game_over, (WIDTH//2 - 80, HEIGHT//2 - 40))
            self.screen.blit(score_text, (WIDTH//2 - 60, HEIGHT//2))
            self.screen.blit(restart, (WIDTH//2 - 80, HEIGHT//2 + 40))
            
        else:
            # Game screen
            # Draw snake (circles for realistic look)
            for i, (x, y) in enumerate(self.snake):
                center_x = x * GRID_SIZE + GRID_SIZE//2
                center_y = y * GRID_SIZE + GRID_SIZE//2
                
                if i == 0:  # Head with eyes
                    pygame.draw.circle(self.screen, GREEN, (center_x, center_y), GRID_SIZE//2)
                    # Simple eyes
                    eye_color = BLACK
                    if self.direction == DIRS['UP']:
                        pygame.draw.circle(self.screen, eye_color, (center_x-4, center_y-4), 2)
                        pygame.draw.circle(self.screen, eye_color, (center_x+4, center_y-4), 2)
                    elif self.direction == DIRS['DOWN']:
                        pygame.draw.circle(self.screen, eye_color, (center_x-4, center_y+4), 2)
                        pygame.draw.circle(self.screen, eye_color, (center_x+4, center_y+4), 2)
                    elif self.direction == DIRS['LEFT']:
                        pygame.draw.circle(self.screen, eye_color, (center_x-4, center_y-4), 2)
                        pygame.draw.circle(self.screen, eye_color, (center_x-4, center_y+4), 2)
                    else:  # RIGHT
                        pygame.draw.circle(self.screen, eye_color, (center_x+4, center_y-4), 2)
                        pygame.draw.circle(self.screen, eye_color, (center_x+4, center_y+4), 2)
                else:  # Body
                    color = GREEN if i % 2 == 0 else (0, 200, 0)
                    pygame.draw.circle(self.screen, color, (center_x, center_y), GRID_SIZE//2)
            
            # Draw food
            food_x, food_y = self.food
            pygame.draw.circle(self.screen, RED, 
                             (food_x * GRID_SIZE + GRID_SIZE//2, 
                              food_y * GRID_SIZE + GRID_SIZE//2), 
                             GRID_SIZE//2)
            
            # UI
            level_text = self.font.render(f"Level: {self.level}", True, YELLOW)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(level_text, (10, 10))
            self.screen.blit(score_text, (10, 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # FPS based on level
            fps = self.levels[self.level] if self.level else 60
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()