import pygame
import sys
import random

# Inicialización
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Completo")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
GRAY = (100, 100, 100)

# Configuración del juego
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 7
INITIAL_BALL_SPEED = 5
MAX_BALL_SPEED = 10

# Estados del juego
MENU = 0
GAME_IA = 1
GAME_COOP = 2
OPTIONS = 3
game_state = MENU

# Configuración de opciones
sound_volume = 1.0  # 100%
fullscreen = False

# Sonidos y música
try:
    # Efectos de sonido
    sound_paddle = pygame.mixer.Sound("paddle.wav")
    sound_wall = pygame.mixer.Sound("wall.wav")
    sound_score = pygame.mixer.Sound("score.wav")
    sound_menu = pygame.mixer.Sound("menu.wav")
    
    # Música de fondo
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.set_volume(0.5)  # Volumen inicial al 50%
    pygame.mixer.music.play(-1)  # Reproducir en loop
except:
    print("Advertencia: No se encontraron algunos archivos de audio")
    sound_paddle = None
    sound_wall = None
    sound_score = None
    sound_menu = None

# Fuentes
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, 2)
        text_surf = font_medium.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        clicked = self.rect.collidepoint(mouse_pos) and mouse_click
        if clicked and sound_menu:
            sound_menu.play()
        return clicked

# Crear botones
buttons_menu = [
    Button(WIDTH//2-150, HEIGHT//2-100, 300, 60, "Jugar vs IA"),
    Button(WIDTH//2-150, HEIGHT//2, 300, 60, "Jugar Cooperativo"),
    Button(WIDTH//2-150, HEIGHT//2+100, 300, 60, "Opciones"),
    Button(WIDTH//2-150, HEIGHT//2+200, 300, 60, "Salir")
]

buttons_options = [
    Button(WIDTH//2-150, HEIGHT//2-100, 300, 60, f"Volumen: {int(sound_volume*100)}%"),
    Button(WIDTH//2-150, HEIGHT//2, 300, 60, f"Pantalla Completa: {'SÍ' if fullscreen else 'NO'}"),
    Button(WIDTH//2-150, HEIGHT//2+100, 300, 60, "Atrás")
]

def reset_game():
    global player_paddle, ai_paddle, ball, player_score, ai_score, ball_speed_x, ball_speed_y
    
    player_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    player_score = 0
    ai_score = 0
    ball_speed_x = INITIAL_BALL_SPEED * random.choice((1, -1))
    ball_speed_y = INITIAL_BALL_SPEED * random.choice((1, -1))

def update_volume():
    # Efectos de sonido
    if sound_paddle:
        sound_paddle.set_volume(sound_volume)
    if sound_wall:
        sound_wall.set_volume(sound_volume)
    if sound_score:
        sound_score.set_volume(sound_volume)
    if sound_menu:
        sound_menu.set_volume(sound_volume)
    
    # Música de fondo
    pygame.mixer.music.set_volume(sound_volume * 0.5)  # La música al 50% del volumen general

def draw_menu():
    screen.fill(BLACK)
    title = font_large.render("PONG", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    for button in buttons_menu:
        button.draw(screen)

def draw_options():
    screen.fill(BLACK)
    title = font_large.render("OPCIONES", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    for button in buttons_options:
        button.draw(screen)

def draw_game():
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, BLUE, player_paddle)
    pygame.draw.rect(screen, RED, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    player_text = font_large.render(str(player_score), True, BLUE)
    ai_text = font_large.render(str(ai_score), True, RED)
    screen.blit(player_text, (WIDTH//4, 20))
    screen.blit(ai_text, (3*WIDTH//4, 20))

def toggle_fullscreen():
    global fullscreen, screen, WIDTH, HEIGHT
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Inicialización del juego
reset_game()
update_volume()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state in (GAME_IA, GAME_COOP):
                game_state = MENU
    
    # Lógica del menú
    if game_state == MENU:
        for button in buttons_menu:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if button.text == "Jugar vs IA":
                    game_state = GAME_IA
                    reset_game()
                elif button.text == "Jugar Cooperativo":
                    game_state = GAME_COOP
                    reset_game()
                elif button.text == "Opciones":
                    game_state = OPTIONS
                elif button.text == "Salir":
                    running = False
    
    # Lógica de opciones
    elif game_state == OPTIONS:
        for button in buttons_options:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if button.text.startswith("Volumen"):
                    sound_volume = (sound_volume + 0.2) % 1.2
                    if sound_volume == 0: sound_volume = 0.2
                    update_volume()
                    button.text = f"Volumen: {int(sound_volume*100)}%"
                elif button.text.startswith("Pantalla"):
                    toggle_fullscreen()
                    button.text = f"Pantalla Completa: {'SÍ' if fullscreen else 'NO'}"
                elif button.text == "Atrás":
                    game_state = MENU
    
    # Lógica del juego
    elif game_state in (GAME_IA, GAME_COOP):
        keys = pygame.key.get_pressed()
        
        # Control jugador 1 (W/S)
        if keys[pygame.K_w] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED
        
        # Control jugador 2 (Flechas) o IA
        if game_state == GAME_COOP:
            if keys[pygame.K_UP] and ai_paddle.top > 0:
                ai_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and ai_paddle.bottom < HEIGHT:
                ai_paddle.y += PADDLE_SPEED
        else:
            # IA simple
            if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
                ai_paddle.y += PADDLE_SPEED - 1
            if ai_paddle.centery > ball.centery and ai_paddle.top > 0:
                ai_paddle.y -= PADDLE_SPEED - 1
        
        # Movimiento de la pelota
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        
        # Colisiones con bordes
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
            if sound_wall:
                sound_wall.play()
        
        # Colisiones con paletas
        if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
            ball_speed_x *= -1.1
            ball_speed_y *= 1.1
            ball_speed_x = max(-MAX_BALL_SPEED, min(MAX_BALL_SPEED, ball_speed_x))
            ball_speed_y = max(-MAX_BALL_SPEED, min(MAX_BALL_SPEED, ball_speed_y))
            if sound_paddle:
                sound_paddle.play()
        
        # Puntuación
        if ball.left <= 0:
            ai_score += 1
            ball_speed_x, ball_speed_y = INITIAL_BALL_SPEED * random.choice((1, -1)), INITIAL_BALL_SPEED * random.choice((1, -1))
            ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
            if sound_score:
                sound_score.play()
        
        if ball.right >= WIDTH:
            player_score += 1
            ball_speed_x, ball_speed_y = INITIAL_BALL_SPEED * random.choice((1, -1)), INITIAL_BALL_SPEED * random.choice((1, -1))
            ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
            if sound_score:
                sound_score.play()
    
    # Dibujado
    if game_state == MENU:
        draw_menu()
    elif game_state == OPTIONS:
        draw_options()
    else:
        draw_game()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()