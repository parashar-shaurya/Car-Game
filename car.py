import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race Game")

GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

player_width = 50
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120
player_speed = 7

enemies = []
game_speed = 5
score = 0
game_over = False
spawn_timer = 0
road_line_offset = 0

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 74)

class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = random.randint(ROAD_LEFT + 25, ROAD_RIGHT - 25 - self.width)
        self.y = -self.height
        self.color = RED

    def move(self, speed):
        self.y += speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def reset_game():
    global player_x, enemies, game_speed, score, game_over, spawn_timer

    player_x = WIDTH // 2 - player_width // 2
    enemies = []
    game_speed = 5
    score = 0
    game_over = False
    spawn_timer = 0

def draw_road():
    global road_line_offset

    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5)

    road_line_offset += game_speed

    if road_line_offset >= 40:
        road_line_offset = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y + road_line_offset, 10, 20))

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height), 2)

    pygame.draw.rect(screen, BLACK, (player_x + 5, player_y + 10, player_width - 10, 20))
    pygame.draw.rect(screen, BLACK, (player_x + 5, player_y + 50, player_width - 10, 15))

print("Car Race Game Started!")
print("Controls: LEFT/RIGHT arrow keys to move")
print("Avoid the red cars!")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()
                print("Game restarted!")

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > ROAD_LEFT:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < ROAD_RIGHT - player_width:
            player_x += player_speed

        spawn_timer += 1

        if spawn_timer > max(30, 60 - score // 50):
            enemies.append(Enemy())
            spawn_timer = 0

        for enemy in enemies[:]:
            enemy.move(game_speed)

            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            if player_rect.colliderect(enemy.get_rect()):
                game_over = True
                print(f"Crash! Game Over! Final Score: {score}")

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 10

        score += 1

        if score % 100 == 0:
            game_speed += 0.5
            print(f"Speed increased! New speed: {game_speed}")

    screen.fill(BLACK)

    draw_road()
    draw_player()

    for enemy in enemies:
        enemy.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    speed_text = font.render(f"Speed: {game_speed:.1f}", True, YELLOW)
    screen.blit(speed_text, (10, 50))

    controls_text = font.render("LEFT/RIGHT arrows", True, WHITE)
    screen.blit(controls_text, (WIDTH - 180, 10))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        game_over_text = large_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 100))

        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))

        restart_text = font.render("Press R to Restart", True, GREEN)
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()