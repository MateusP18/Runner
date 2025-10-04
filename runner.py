import pygame
import random
import sys

# --- Configurações ---
WIDTH, HEIGHT = 800, 300
GROUND_Y = HEIGHT - 40
FPS = 60

# Dino
DINO_X = 50
DINO_WIDTH, DINO_HEIGHT = 44, 44
JUMP_VELOCITY = -14
GRAVITY = 0.7

# Obstáculos
OB_WIDTH, OB_HEIGHT = 30, 40
OB_SPEED_START = 6

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (83, 180, 70)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner - Versão Simples")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# --- Estado do jogador (dino) ---
dino_rect = pygame.Rect(DINO_X, GROUND_Y - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT)
dino_vel_y = 0
on_ground = True

# Obstáculos: lista de rects
obstacles = []

# Timer para spawn de obstáculos
SPAWN_OB = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OB, random.randint(900, 1600))

score = 0
speed = OB_SPEED_START
game_over = False

def reset_game():
    global dino_rect, dino_vel_y, on_ground, obstacles, score, speed, game_over
    dino_rect = pygame.Rect(DINO_X, GROUND_Y - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT)
    dino_vel_y = 0
    on_ground = True
    obstacles = []
    score = 0
    speed = OB_SPEED_START
    game_over = False
    pygame.time.set_timer(SPAWN_OB, random.randint(900, 1600))

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Loop principal
while True:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWN_OB and not game_over:
            h = OB_HEIGHT
            rect = pygame.Rect(WIDTH, GROUND_Y - h, OB_WIDTH, h)
            obstacles.append(rect)
            pygame.time.set_timer(SPAWN_OB, random.randint(700, 1600))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not game_over and on_ground:
                    dino_vel_y = JUMP_VELOCITY
                    on_ground = False
                elif game_over:
                    reset_game()

            if event.key == pygame.K_r and game_over:
                reset_game()

    # Física do dino
    if not on_ground:
        dino_vel_y += GRAVITY
        dino_rect.y += int(dino_vel_y)
        if dino_rect.bottom >= GROUND_Y:
            dino_rect.bottom = GROUND_Y
            dino_vel_y = 0
            on_ground = True

    # Move obstáculos
    if not game_over:
        for ob in obstacles:
            ob.x -= int(speed)
        obstacles = [o for o in obstacles if o.right > -50]

        for ob in obstacles:
            if dino_rect.colliderect(ob):
                game_over = True

        score += round(dt * 0.01)
        if score % 200 == 0 and score != 0:
            speed = OB_SPEED_START + (score // 200)

    # Desenhar
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

    pygame.draw.rect(screen, BLACK, dino_rect)
    eye_rect = pygame.Rect(dino_rect.x + DINO_WIDTH - 12, dino_rect.y + 10, 6, 6)
    pygame.draw.rect(screen, WHITE, eye_rect)

    for ob in obstacles:
        pygame.draw.rect(screen, GREEN, ob)
        pygame.draw.rect(screen, BLACK, (ob.x + 4, ob.y + 6, 6, 6))

    draw_text(f"Pontos: {score}", WIDTH - 150, 10)

    if game_over:
        draw_text("GAME OVER - Aperte Espaço ou R para reiniciar", WIDTH//2 - 230, HEIGHT//2 - 10, (200, 20, 20))
        draw_text(f"Pontos finais: {score}", WIDTH//2 - 80, HEIGHT//2 + 20)

    pygame.display.flip()