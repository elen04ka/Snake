import pygame
import sys
from random import randrange

# Ініціалізація Pygame
pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Розміри екрану
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Ініціалізація екрану
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Завантаження фонового зображення
background = pygame.transform.scale(pygame.image.load('background.jpg'), (SCREEN_HEIGHT, SCREEN_WIDTH))

# Шрифти
font = pygame.font.SysFont('Comic Sans MS', 36, bold=True)

# Функція для створення тексту
def create_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    return text_surface, text_rect

# Головний цикл гри
def main_menu():
    menu_items = ["Easy", "Medium", "Hard"]
    selected_item = 0  # Початковий вибраний пункт меню

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Відображення фону меню
        screen.blit(background, (0, 0))

        title_text, title_rect = create_text("Snake Game", BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        screen.blit(title_text, title_rect)

        # Відображення пунктів меню та позначення вибраного пункту
        for i, item in enumerate(menu_items):
            color = WHITE if i == selected_item else BLACK
            item_text, item_rect = create_text(item, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
            screen.blit(item_text, item_rect)

        pygame.display.flip()

        # Обробка клавіш w та s для перемикання по пунктах меню
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_s:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    start_game(menu_items[selected_item])

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Код гри

RES = 700
SIZE = 50
x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
dris = {'W': True, 'S': True, 'A': True, 'D': True}
length = 1
snake = [(x, y)]
dx, dy = 0, 0
fps = 8
score = 0
paused = False
game_over = False
game_over_on_wall_collision = False

pygame.mixer.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Comic Sans MS', 26, bold=True)
font_end = pygame.font.SysFont('Comic Sans MS', 70, bold=True)
font_pause = pygame.font.SysFont('Comic Sans MS', 25, bold=True)

apple_texture = pygame.image.load('apple_texture.png')
snake_head_texture = pygame.image.load('snake_head_texture.png')
snake_body_texture = pygame.image.load('snake_body_texture.png')

pygame.mixer.music.load('background_music.mp3')
game_over_sound = pygame.mixer.Sound('game_over_sound.mp3')

def reset_game():
    global x, y, apple, dris, length, snake, dx, dy, score, paused, game_over
    x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    dris = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    score = 0
    paused = False
    game_over = False

def start_game(difficulty):
    global game_over_on_wall_collision, fps
    if difficulty == "Easy":
        fps = 8
        game_over_on_wall_collision = False
    elif difficulty == "Medium":
        fps = 12
        game_over_on_wall_collision = False
    elif difficulty == "Hard":
        fps = 14
        game_over_on_wall_collision = True

    reset_game()
    main_loop()

def main_loop():
    global x, y, apple, dris, length, snake, dx, dy, fps, score, paused, game_over, game_over_on_wall_collision

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_b:
                    game_over == True
                    main_menu()
                elif game_over and event.key == pygame.K_RETURN:
                    reset_game()

        key = pygame.key.get_pressed()
        if not paused and not game_over:
            if key[pygame.K_w] and dris['W']:
                dris = {'W': True, 'S': False, 'A': True, 'D': True}
                dx, dy = 0, -1
            if key[pygame.K_s] and dris['S']:
                dx, dy = 0, 1
                dris = {'W': False, 'S': True, 'A': True, 'D': True}
            if key[pygame.K_a] and dris['A']:
                dx, dy = -1, 0
                dris = {'W': True, 'S': True, 'A': True, 'D': False}
            if key[pygame.K_d] and dris['D']:
                dx, dy = 1, 0
                dris = {'W': True, 'S': True, 'A': False, 'D': True}

            sc.fill(pygame.Color('black'))

            if snake[0] == apple:
                apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                score += 1
                snake.append((0, 0))
                length += 1

            for i in range(length - 1, 0, -1):
                snake[i] = (snake[i-1][0], snake[i-1][1])

            x += dx * SIZE
            y += dy * SIZE

            if x < 0:
                x = RES - SIZE
            elif x > RES - SIZE:
                x = 0
            elif y < 0:
                y = RES - SIZE
            elif y > RES - SIZE:
                y = 0

            snake[0] = (x, y)

            if game_over_on_wall_collision and (x < 0 or x >= RES or y < 0 or y >= RES):
                game_over = True
                pygame.mixer.music.stop()
                game_over_sound.play()

            for segment in snake[1:]:
                if snake[0] == segment:
                    game_over = True
                    pygame.mixer.music.stop()
                    game_over_sound.play()

            for i, segment in enumerate(snake):
                if i == 0:
                    sc.blit(snake_head_texture, (*segment, SIZE, SIZE))
                else:
                    sc.blit(snake_body_texture, (*segment, SIZE, SIZE))

            sc.blit(apple_texture, (*apple, SIZE, SIZE))

        if game_over:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('white'))
            sc.blit(render_end, (RES // 2 - 200, RES // 2.5))
            render_restart = font_score.render('Press ENTER to restart', 1, pygame.Color('white'))
            sc.blit(render_restart, (RES // 1.63 - 250, RES // 2.5 + 80))

        if paused:
            render_pause = font_end.render('PAUSE', 1, pygame.Color('white'))
            sc.blit(render_pause, (RES // 1.9 - 150, RES // 2.3))

        if not game_over:
            render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('white'))
            sc.blit(render_score, (5, 5))

            render_paused = font_pause.render('Press P to pause the game', 1, pygame.Color('white'))
            sc.blit(render_paused, (RES - 330, 5))

            back_to_menu = font_pause.render('Press B to back to menu', 1, pygame.Color('white'))
            sc.blit(back_to_menu, (RES - 330, 30))

        if not paused and not game_over and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        pygame.display.flip()
        clock.tick(fps)

# Основний цикл меню
if __name__ == "__main__":
    main_menu()
