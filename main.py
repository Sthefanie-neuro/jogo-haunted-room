import pgzrun
import random
import glob
import math
import os
from pygame import Rect

# --- Configurações da Janela ---
WIDTH = 800
HEIGHT = 600
TITLE = "Haunted Room"
FONT_NAME = "creepster" # Nome do arquivo da fonte 

# --- Variáveis Globais do Jogo ---
game_state = "MENU"
is_music_on = True
level = 1
gems_collected = 0
high_score = 0
enemies_per_level = 2
enemy_speed_base = 0.8
show_exit_message = False

# --- Função Auxiliar para Carregar Sprites ---
def load_variants(patterns):
    """
    Carrega uma lista de nomes de arquivos de imagem a partir de uma lista de padrões glob.
    Isso permite encontrar arquivos em subpastas, como 'hero/walking_left/*.png'.
    """
    files = []
    for pattern in patterns:
        # pgzrun procura imagens na pasta 'images/' por padrão
        # Usamos os.path.join para compatibilidade entre sistemas (Windows/Linux/Mac)
        full_pattern = os.path.join('images', pattern)
        found_files = glob.glob(full_pattern)

        for f in found_files:
            # Normaliza as barras para '/' e remove o prefixo 'images/'
            relative_path = f.replace('\\', '/').replace('images/', '')
            files.append(relative_path)

    # Usa set para remover duplicatas e sorted para garantir uma ordem consistente
    return sorted(list(set(files)))

# --- Sprites e Assets do Menu ---
# Usamos try-except para o caso de as imagens não existirem, o jogo ainda rodará
try:
    start_button = Actor('button_start', (WIDTH / 2, HEIGHT / 2 - 100))
    music_button = Actor('button_music', (WIDTH / 2, HEIGHT / 2))
    instructions_button = Actor('instructions', (WIDTH / 2, HEIGHT / 2 + 100))
    # MUDANÇA: Posição do botão de sair ajustada para o canto inferior direito
    quit_button = Actor('button_quit', (WIDTH - 100, HEIGHT - 60))
    key_icons = Actor('key_icons', (WIDTH - 100, HEIGHT - 100))
except Exception:
    print("Aviso: Sprites dos botões do menu não encontradas. Os botões serão exibidos como retângulos.")
    start_button = Rect((WIDTH / 2 - 100, HEIGHT / 2 - 125), (200, 50))
    music_button = Rect((WIDTH / 2 - 100, HEIGHT / 2 - 25), (200, 50))
    instructions_button = Rect((WIDTH / 2 - 100, HEIGHT / 2 + 75), (200, 50))
    quit_button = Rect(0, 0, 200, 50)
    quit_button.center = (WIDTH - 100, HEIGHT - 60)
    key_icons = Rect(WIDTH - 150, HEIGHT - 150, 100, 100)


# --- Objetos do Jogo ---
player = None
enemies = []
gems = []
door = None

# --- Classes do Jogo ---
class Character:
    """Classe base para todos os personagens (jogador e inimigos)."""
    def __init__(self, x, y, sprite_folder, animation_speed=10):
        self.animation_speed = animation_speed
        self.frame_counter = 0
        self.current_frame = 0
        self.direction = "right"  # pode ser: left/right/up/down
        self.state = "idle"       # pode ser: idle/walking/attacking/etc.
        self.is_moving = False

        sf = sprite_folder
        self.animations = {
            "up":    load_variants([f"{sf}/hero_move_up/*.png", f"{sf}/up/*.png"]),
            "down":  load_variants([f"{sf}/hero_move_down/*.png", f"{sf}/down/*.png"]),
            "left":  load_variants([f"{sf}/hero_move_left/*.png", f"{sf}/left/*.png"]),
            "right": load_variants([f"{sf}/hero_move_right/*.png", f"{sf}/right/*.png"]),
            "walking_left":  load_variants([f"{sf}/walking_left/*.png"]),
            "walking_right": load_variants([f"{sf}/walking_right/*.png"]),
            "attacking_left":  load_variants([f"{sf}/attacking_left/*.png"]),
            "attacking_right": load_variants([f"{sf}/attacking_right/*.png"]),
            "taunt_left":  load_variants([f"{sf}/taunt_left/*.png"]),
            "taunt_right": load_variants([f"{sf}/taunt_right/*.png"]),
            "idle_left":  load_variants([f"{sf}/idle_left/*.png", f"{sf}/idle/*_left.png"]),
            "idle_right": load_variants([f"{sf}/idle_right/*.png", f"{sf}/idle/*_right.png"]),
            "idle_up":    load_variants([f"{sf}/idle_up/*.png", f"{sf}/idle/*_up.png"]),
            "idle_down":  load_variants([f"{sf}/idle_down/*.png", f"{sf}/idle/*_down.png"]),
            "move": load_variants([f"{sf}/move/*.png"]),
            "walking": load_variants([f"{sf}/walking/*.png"]),
            "idle": load_variants([f"{sf}/idle/*.png"]),
        }

        # Tenta encontrar uma animação inicial para o personagem
        initial_animation = (
            self.animations.get("idle_right") or
            self.animations.get("idle") or
            self.animations.get("right") or
            self.animations.get("move")
        )
        if not initial_animation:
            print(f"Erro: Não foi possível carregar sprites de '{sprite_folder}'. Verifique a pasta e nomes.")
            raise FileNotFoundError(f"Sprites não encontradas para {sprite_folder}")

        self.actor = Actor(initial_animation[0])
        self.actor.pos = (x, y)

        # Define o retângulo de colisão com base no tamanho do sprite (com uma pequena escala)
        scale_factor = 0.6
        rect_width = self.actor.width * scale_factor
        rect_height = self.actor.height * scale_factor
        self.rect = Rect(0, 0, rect_width, rect_height)
        self.rect.center = (x, y)

    def _pick_sprites(self):
        """Escolhe a lista de sprites correta com base no estado e direção."""
        # Tenta encontrar a animação mais específica primeiro (ex: "walking_right")
        # Se não encontrar, tenta uma mais genérica (ex: "right" ou "walking")
        if self.is_moving:
            candidates = [f"{self.state}_{self.direction}", self.direction, self.state, "move", "walking"]
        else: # not moving
            candidates = [f"idle_{self.direction}", "idle", self.direction, "down"]

        for key in candidates:
            sprites = self.animations.get(key)
            if sprites:
                return sprites
        return None # Retorna None se nenhuma animação for encontrada

    def update_animation(self):
        """Atualiza o frame da animação atual."""
        self.frame_counter += 1
        sprites_to_use = self._pick_sprites()

        if sprites_to_use and self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(sprites_to_use)
            self.actor.image = sprites_to_use[self.current_frame]

    def draw(self):
        """Desenha o personagem na tela."""
        self.actor.pos = self.rect.center
        self.actor.draw()


class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'hero', animation_speed=5)
        self.speed = 2
        # Atributos para o bônus de velocidade
        self.speed_boost = 0
        self.boost_timer = 0

    def apply_boost(self):
        """Aplica o bônus de velocidade e define o temporizador."""
        self.speed_boost = 1.5  # Aumenta a velocidade em 1.5
        self.boost_timer = 120  # 120 frames = 2 segundos a 60 FPS

    def move(self):
        # Lógica para o temporizador do bônus de velocidade
        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.speed_boost = 0

        self.is_moving = False
        current_speed = self.speed + self.speed_boost
        
        if keyboard.up and self.rect.top > 0:
            self.rect.y -= current_speed
            self.is_moving = True
            self.direction = "up"
        elif keyboard.down and self.rect.bottom < HEIGHT:
            self.rect.y += current_speed
            self.is_moving = True
            self.direction = "down"
        elif keyboard.left and self.rect.left > 0:
            self.rect.x -= current_speed
            self.is_moving = True
            self.direction = "left"
        elif keyboard.right and self.rect.right < WIDTH:
            self.rect.x += current_speed
            self.is_moving = True
            self.direction = "right"

        self.state = "walking" if self.is_moving else "idle"
        self.update_animation()


class Bat(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'bat', animation_speed=8)
        self.speed = enemy_speed_base + (level * 0.15)
        self.vx = random.choice([-self.speed, self.speed])
        self.vy = random.choice([-self.speed, self.speed])

    def move_ai(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        self.direction = "right" if self.vx > 0 else "left"

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy
        
        self.is_moving = True
        self.state = "walking"
        self.update_animation()


class Wraith1(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'wraith_01', animation_speed=10)
        self.speed = enemy_speed_base + (level * 0.1)
        self.vx = random.choice([-self.speed, self.speed])
        self.vy = random.choice([-self.speed, self.speed])

    def move_ai(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        self.direction = "right" if self.vx > 0 else "left"

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

        self.is_moving = True
        self.state = "walking"
        self.update_animation()


class Wraith2(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'wraith_02', animation_speed=8)
        self.speed = enemy_speed_base * 0.8 + (level * 0.1) # Persegue o jogador

    def move_ai(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        self.is_moving = dist > 5

        if self.is_moving:
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist
            self.state = "attacking"
        else:
            self.state = "idle"
        
        self.direction = "right" if dx > 0 else "left"
        self.update_animation()


class Wraith3(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'wraith_03', animation_speed=15)
        self.speed = enemy_speed_base + (level * 0.1)
        self.state = "walking"
        self.state_timer = 0
        self.state_duration = random.randint(120, 240) # Duração do estado
        self.vx = random.choice([-self.speed, self.speed])
        self.vy = random.choice([-self.speed, self.speed])

    def move_ai(self):
        self.state_timer += 1
        
        if self.state == "walking":
            self.is_moving = True
            self.rect.x += self.vx
            self.rect.y += self.vy
            
            self.direction = "right" if self.vx > 0 else "left"

            if self.rect.left <= 0 or self.rect.right >= WIDTH: self.vx *= -1
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT: self.vy *= -1

            if self.state_timer >= self.state_duration:
                self.state = "taunt"
                self.state_timer = 0
                self.state_duration = random.randint(60, 120)

        elif self.state == "taunt":
            self.is_moving = False
            if self.state_timer >= self.state_duration:
                self.state = "walking"
                self.vx = random.choice([-self.speed, self.speed])
                self.vy = random.choice([-self.speed, self.speed])
                self.state_timer = 0
                self.state_duration = random.randint(120, 240)
        
        self.update_animation()


class Gem(Actor):
    def __init__(self, x, y):
        super().__init__('gem', (x, y))

# --- Funções de Gerenciamento do Jogo ---

def load_high_score():
    global high_score
    try:
        with open("score.txt", "r") as f:
            high_score = int(f.read())
    except (FileNotFoundError, ValueError):
        high_score = 0

def save_high_score():
    global high_score
    if gems_collected > high_score:
        high_score = gems_collected
        with open("score.txt", "w") as f:
            f.write(str(high_score))

def reset_game():
    global game_state, player, enemies, gems, level, gems_collected
    game_state = "PLAYING"
    level = 1
    gems_collected = 0
    player = Player(WIDTH / 2, HEIGHT / 2)
    spawn_objects()
    if is_music_on:
        try:
            music.set_volume(0.5)
            music.play('background2.wav')
        except Exception as e:
            print(f"Aviso: Não foi possível tocar a música 'background2.wav'. Erro: {e}")

def hide_exit_message():
    global show_exit_message
    show_exit_message = False

def spawn_objects():
    global enemies, gems
    enemies.clear()
    gems.clear()

    num_enemies = 2 + (level - 1)
    enemy_types = [Bat, Wraith1, Wraith2, Wraith3]

    for _ in range(num_enemies):
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            dist = math.hypot(x - player.rect.centerx, y - player.rect.centery)
            if dist > 200: # Nasce longe do jogador
                enemy_class = random.choice(enemy_types)
                enemies.append(enemy_class(x, y))
                break

    for _ in range(5):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        gems.append(Gem(x, y))

def next_level():
    global level
    try:
        sounds.level_up.play()
    except Exception:
        print("Aviso: Arquivo de som 'level_up.wav' não encontrado.")

    level += 1
    player.rect.center = (50, HEIGHT / 2)
    spawn_objects()

# --- Funções Principais do Pygame Zero (draw, update, on_mouse_down) ---

def draw():
    if game_state == "MENU":
        draw_menu()
    elif game_state == "PLAYING":
        screen.blit('caverna_background', (0, 0))
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for gem in gems:
            gem.draw()

        if show_exit_message:
            screen.draw.text("Colete todas as gemas para sair!", center=(WIDTH/2, HEIGHT - 50), color="yellow", fontsize=40, owidth=1, ocolor="black", fontname=FONT_NAME)

        screen.draw.text(f"Nível: {level}", (10, 10), color="white", fontsize=20, fontname=FONT_NAME)
        screen.draw.text(f"Gemas: {gems_collected}", (10, 35), color="yellow", fontsize=20, fontname=FONT_NAME)
        screen.draw.text(f"Recorde: {high_score}", (10, 60), color="cyan", fontsize=20, fontname=FONT_NAME)
    elif game_state == "GAME_OVER":
        draw_game_over()
    elif game_state == "INSTRUCTIONS":
        draw_instructions()

def update():
    global game_state
    if game_state == "PLAYING":
        player.move()
        for enemy in enemies:
            enemy.move_ai()
        check_collisions()
    elif game_state in ("GAME_OVER", "INSTRUCTIONS"):
        if keyboard.escape:
            game_state = "MENU"
            music.stop()

def on_mouse_down(pos):
    global game_state, is_music_on
    if game_state == "MENU":
        if start_button.collidepoint(pos):
            reset_game()
        elif music_button.collidepoint(pos):
            is_music_on = not is_music_on
            if is_music_on:
                music.unpause()
            else:
                music.pause()
        elif instructions_button.collidepoint(pos):
            game_state = "INSTRUCTIONS"
        elif quit_button.collidepoint(pos):
            exit()

def check_collisions():
    global game_state, gems_collected, show_exit_message
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            game_state = "GAME_OVER"
            save_high_score()
            try: sounds.collision.play()
            except Exception: print("Aviso: Som 'collision.wav' não encontrado.")
            music.stop()

    for gem in list(gems):
        if player.rect.colliderect(gem._rect):
            gems.remove(gem)
            gems_collected += 1
            player.apply_boost() # Aplica o bônus de velocidade
            try: sounds.score_sound.play()
            except Exception: print("Aviso: Som 'score_sound.wav' não encontrado.")

    exit_zone = Rect(WIDTH - 50, 0, 50, HEIGHT)
    if player.rect.colliderect(exit_zone):
        if len(gems) == 0:
            next_level()
        else:
            show_exit_message = True
            clock.schedule_unique(hide_exit_message, 2.0)

# --- Funções de Desenho de Telas ---

def draw_menu():
    screen.blit('menu_background', (0, 0))
    screen.draw.text(TITLE, center=(WIDTH/2, 100), color="white", fontsize=80, owidth=1.5, ocolor="black", fontname=FONT_NAME)
    
    start_button.draw()
    music_button.image = 'button_music' if is_music_on else 'button_music_off'
    music_button.draw()
    instructions_button.draw()
    quit_button.draw()

    screen.draw.text(f"Recorde: {high_score}", center=(WIDTH/2, HEIGHT - 50), color="cyan", fontsize=40, fontname=FONT_NAME)

def draw_game_over():
    screen.blit('game_over', (0, 0))
    screen.draw.text(f"Gemas Coletadas: {gems_collected}", center=(WIDTH/2, HEIGHT/2 + 20), color="yellow", fontsize=50, fontname=FONT_NAME)
    screen.draw.text(f"Recorde: {high_score}", center=(WIDTH/2, HEIGHT/2 + 70), color="white", fontsize=40, fontname=FONT_NAME)
    screen.draw.text("Pressione ESC para voltar ao menu", center=(WIDTH/2, HEIGHT - 50), color="white", fontsize=35, fontname=FONT_NAME)

def draw_instructions():
    screen.blit('menu_background', (0, 0))
    
    instructions_text = "Aventureiro, sua missão é coletar todas as gemas para destravar a passagem secreta à direita da sala. Mas cuidado! Monstros protegem o tesouro e se tornam mais fortes a cada nível."
    key_text = "Colete gemas para um impulso de velocidade e use as setas do teclado para escapar!"

    screen.draw.textbox(instructions_text, Rect(100, 150, WIDTH-200, 200), color="white", fontname=FONT_NAME)
    screen.draw.textbox(key_text, Rect(100, 350, WIDTH-200, 100), color="white", fontname=FONT_NAME)
    
    key_icons.pos = (WIDTH / 2, HEIGHT / 2 + 180)
    key_icons.draw()
    
    screen.draw.text("Pressione ESC para voltar", center=(WIDTH/2, HEIGHT - 50), color="cyan", fontsize=25, fontname=FONT_NAME)

# --- Inicialização ---
load_high_score()
pgzrun.go()