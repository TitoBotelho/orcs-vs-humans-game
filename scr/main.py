#imagens:
# https://zerie.itch.io/tiny-rpg-character-asset-pack
# https://www.piskelapp.com/p/create/sprite/

import pgzrun
import random
import math

WIDTH = 800
HEIGHT = 600

player_speed = 3
PLAYER_HIT_COOLDOWN = 30  # frames de invencibilidade após levar dano (~0.5s a 60fps)
ORC_ATTACK_DELAY = 5     # frames de espera antes do ataque do orc (~0.5s a 60fps)

# Número inicial de orcs
wave_count = 1

# Animações do jogador (normais e invertidas)
IDLE_FRAMES = [f"soldier-idle-{i}" for i in range(1, 7)]
WALK_FRAMES = [f"soldier-walk-{i}" for i in range(1, 7)]
ATTACK_FRAMES = [f"soldier-attack-{i}" for i in range(1, 7)]
IDLE_FRAMES_E = [f"soldier-idle-e-{i}" for i in range(1, 7)]
WALK_FRAMES_E = [f"soldier-walk-e-{i}" for i in range(1, 7)]
ATTACK_FRAMES_E = [f"soldier-attack-e-{i}" for i in range(1, 7)]
DEATH_FRAMES = [f"soldier-death-{i}" for i in range(1, 7)]
DEATH_FRAMES_E = [f"soldier-death-e-{i}" for i in range(1, 7)]
HURT_FRAMES = [f"soldier-hurt-{i}" for i in range(1, 7)]
HURT_FRAMES_E = [f"soldier-hurt-e-{i}" for i in range(1, 7)]

# Animações do orc (incluindo ataque)
ORC_IDLE_FRAMES = [f"orc-idle-{i}" for i in range(1, 7)]
ORC_IDLE_FRAMES_E = [f"orc-idle-e-{i}" for i in range(1, 7)]
ORC_WALK_FRAMES = [f"orc-walk-{i}" for i in range(1, 7)]
ORC_WALK_FRAMES_E = [f"orc-walk-e-{i}" for i in range(1, 7)]
ORC_ATTACK_FRAMES = [f"orc-attack-{i}" for i in range(1, 7)]
ORC_ATTACK_FRAMES_E = [f"orc-attack-e-{i}" for i in range(1, 7)]
ORC_DEATH_FRAMES = [f"orc-death-{i}" for i in range(1, 7)]
ORC_DEATH_FRAMES_E = [f"orc-death-e-{i}" for i in range(1, 7)]

# Parâmetros do orc
ORC_ANIM_SPEED = 8
ORC_SPEED = 1.5
ORC_REMOVE_DELAY = 60
ORC_BLINK_DURATION = 60
ORC_BLINK_INTERVAL = 6

MELEE_RANGE = 40

class Orc:
    def __init__(self, x, y):
        # Inicializa o orc na posição (x, y) com animação idle
        self.actor = Actor(ORC_IDLE_FRAMES[0], pos=(x, y))
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = ORC_ANIM_SPEED
        self.speed = ORC_SPEED
        self.is_moving = False
        self.facing_left = False

        self.is_dead = False
        self.death_anim_index = 0
        self.death_anim_timer = 0
        self.death_anim_speed = ORC_ANIM_SPEED
        self.dead_time = 0
        self.blink_timer = 0
        self.visible = True

        self.already_hit = False  # Evita múltiplos hits no mesmo ataque

        # Controle de ataque do orc
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_anim_index = 0
        self.attack_anim_speed = 5
        self.attack_delay_timer = 0
        self.player_in_range = False

    def update(self, player):
        if not self.is_dead:
            dx = player.x - self.actor.x
            dy = player.y - self.actor.y
            dist = math.hypot(dx, dy)

            # Checa se o jogador está ao alcance para ataque
            if dist < MELEE_RANGE:
                self.is_moving = False
                self.player_in_range = True
                if not self.is_attacking:
                    self.attack_delay_timer += 1
                    if self.attack_delay_timer >= ORC_ATTACK_DELAY:
                        self.is_attacking = True
                        self.attack_anim_index = 0
                        self.attack_timer = 0
                        self.attack_delay_timer = 0
            else:
                self.is_moving = True
                self.player_in_range = False
                self.attack_delay_timer = 0
                self.is_attacking = False
                self.attack_anim_index = 0
                self.attack_timer = 0

            # Movimento do orc em direção ao jogador
            if self.is_moving:
                dir_x = dx / dist
                dir_y = dy / dist
                self.actor.x += dir_x * self.speed
                self.actor.y += dir_y * self.speed
                self.facing_left = (player.x < self.actor.x)

            # Animações do orc
            if self.is_attacking:
                self.attack_timer += 1
                if self.attack_timer >= self.attack_anim_speed:
                    self.attack_anim_index += 1
                    self.attack_timer = 0
                    if self.attack_anim_index >= 6:
                        self.attack_anim_index = 0
                        self.is_attacking = False
                if self.facing_left:
                    self.actor.image = ORC_ATTACK_FRAMES_E[self.attack_anim_index]
                else:
                    self.actor.image = ORC_ATTACK_FRAMES[self.attack_anim_index]
            else:
                self.anim_timer += 1
                if self.anim_timer >= self.anim_speed:
                    self.anim_index = (self.anim_index + 1) % 6
                    self.anim_timer = 0
                if self.is_moving:
                    if self.facing_left:
                        self.actor.image = ORC_WALK_FRAMES_E[self.anim_index]
                    else:
                        self.actor.image = ORC_WALK_FRAMES[self.anim_index]
                else:
                    if self.facing_left:
                        self.actor.image = ORC_IDLE_FRAMES_E[self.anim_index]
                    else:
                        self.actor.image = ORC_IDLE_FRAMES[self.anim_index]
        else:
            # Animação de morte do orc
            if self.death_anim_index < 6:
                self.death_anim_timer += 1
                if self.death_anim_timer >= self.death_anim_speed:
                    self.death_anim_index += 1
                    self.death_anim_timer = 0
                    if self.death_anim_index >= 6:
                        self.death_anim_index = 5

            # Após a animação de morte, pisca e desaparece
            if self.death_anim_index == 5:
                self.dead_time += 1
                if self.dead_time > ORC_REMOVE_DELAY:
                    self.blink_timer += 1
                    if self.blink_timer % ORC_BLINK_INTERVAL == 0:
                        self.visible = not self.visible
                    if self.blink_timer > ORC_BLINK_DURATION:
                        self.visible = False

            if self.visible:
                if self.facing_left:
                    self.actor.image = ORC_DEATH_FRAMES_E[self.death_anim_index]
                else:
                    self.actor.image = ORC_DEATH_FRAMES[self.death_anim_index]

    def draw(self):
        # Desenha o orc se estiver visível
        if self.visible:
            self.actor.draw()

    @property
    def x(self):
        return self.actor.x

    @property
    def y(self):
        return self.actor.y

# Parâmetros do jogador e controle de animação
player_anim_index = 0
player_anim_timer = 0
player_anim_speed = 6
attack_anim_speed = 3
player_is_attacking = False
player_attack_timer = 0
player_is_moving = False
player_facing_left = False

player = Actor(IDLE_FRAMES[0], pos=(WIDTH // 2, HEIGHT // 2))

player_life = 3
player_hit_cooldown = 0

# Controle de morte e animação de dano do jogador
player_is_dead = False
player_death_anim_index = 0
player_death_anim_timer = 0
player_death_anim_speed = 6
player_is_hurt = False
player_hurt_anim_index = 0
player_hurt_anim_timer = 0
player_hurt_anim_speed = 4

game_over_timer = 0
GAME_OVER_DURATION = 90  # 1.5 segundos a 60fps

def spawn_wave(count):
    # Cria uma nova horda de orcs, evitando spawn perto do jogador
    new_orcs = []
    for _ in range(count):
        while True:
            x = random.randint(60, WIDTH - 60)
            y = random.randint(60, HEIGHT - 60)
            if abs(x - player.x) > 80 and abs(y - player.y) > 80:
                new_orcs.append(Orc(x, y))
                break
    return new_orcs

orcs = spawn_wave(wave_count)

class Button:
    def __init__(self, text, pos, size=(200, 60)):
        # Inicializa botão do menu
        self.text = text
        self.pos = pos
        self.size = size
        self.rect = Rect((pos[0] - size[0]//2, pos[1] - size[1]//2), size)
        self.hovered = False

    def draw(self):
        # Desenha o botão
        screen.draw.filled_rect(self.rect, (100, 100, 200) if self.hovered else (60, 60, 120))
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(self.text, center=self.rect.center, fontsize=36, color="white")

    def is_clicked(self, pos):
        # Verifica se o botão foi clicado
        return self.rect.collidepoint(pos)

MENU = "menu"
GAME = "game"
EXIT = "exit"
state = MENU

music_on = True

buttons = [
    Button("Start Game", (WIDTH // 2, HEIGHT // 2 - 80)),
    Button("Music: On", (WIDTH // 2, HEIGHT // 2)),
    Button("Exit", (WIDTH // 2, HEIGHT // 2 + 80)),
]

def draw():
    # Desenha a tela do jogo/menu
    screen.clear()
    screen.blit("dungeon_bg", (0, 0))  # Fundo de dungeon
    if state == MENU:
        screen.draw.text("Orcs vs. Humans", center=(WIDTH // 2, 120), fontsize=64, color="yellow")
        for btn in buttons:
            btn.draw()
    elif state == GAME:
        if player_is_dead:
            # Animação de morte do jogador
            frames = DEATH_FRAMES_E if player_facing_left else DEATH_FRAMES
            player.image = frames[min(player_death_anim_index, len(frames) - 1)]
            player.draw()
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=80, color="red")
        else:
            # Animação normal, dano ou ataque do jogador
            if player_is_hurt:
                frames = HURT_FRAMES_E if player_facing_left else HURT_FRAMES
                player.image = frames[min(player_hurt_anim_index, len(frames) - 1)]
            elif player_is_attacking:
                frames = ATTACK_FRAMES_E if player_facing_left else ATTACK_FRAMES
                player.image = frames[min(player_anim_index, len(frames) - 1)]
            elif player_is_moving:
                frames = WALK_FRAMES_E if player_facing_left else WALK_FRAMES
                player.image = frames[player_anim_index]
            else:
                frames = IDLE_FRAMES_E if player_facing_left else IDLE_FRAMES
                player.image = frames[player_anim_index]
            player.draw()
            for orc in orcs:
                orc.draw()
            screen.draw.text(f"Vida: {player_life}", (20, 20), fontsize=40, color="white")
            if player_hit_cooldown > 0:
                screen.draw.text("Invencível!", (20, 60), fontsize=30, color="red")

def on_mouse_move(pos):
    # Destaca botão do menu ao passar o mouse
    if state == MENU:
        for btn in buttons:
            btn.hovered = btn.rect.collidepoint(pos)

def on_mouse_down(pos, button):
    # Lida com cliques do mouse no menu e no jogo
    global state, music_on, player_is_attacking, player_anim_index, player_attack_timer
    if state == MENU:
        if buttons[0].is_clicked(pos):
            state = GAME
            reset_game()
        elif buttons[1].is_clicked(pos):
            music_on = not music_on
            buttons[1].text = f"Music: {'On' if music_on else 'Off'}"
            if music_on:
                music.play("background_music")
            else:
                music.stop()
        elif buttons[2].is_clicked(pos):
            exit()
    elif state == GAME and button == mouse.LEFT and not player_is_attacking and not player_is_dead:
        player_is_attacking = True
        player_anim_index = 0
        player_attack_timer = 0
        sounds.sword_hit.play()  # Toca o som de espadada ao iniciar a animação de ataque

def update():
    # Atualiza o estado do jogo a cada frame
    global player_anim_index, player_anim_timer
    global player_is_moving, player_is_attacking, player_attack_timer, player_facing_left
    global orcs, wave_count, player_life, player_hit_cooldown
    global player_is_dead, player_death_anim_index, player_death_anim_timer, game_over_timer, state
    global player_is_hurt, player_hurt_anim_index, player_hurt_anim_timer

    if state == GAME:
        if player_is_dead:
            # Animação de morte do jogador
            player_death_anim_timer += 1
            if player_death_anim_timer >= player_death_anim_speed:
                player_death_anim_index += 1
                player_death_anim_timer = 0
            if player_death_anim_index >= 6:
                game_over_timer += 1
                if game_over_timer >= GAME_OVER_DURATION:
                    state = MENU
                    reset_game()
            return

        # Atualiza animação de dano, mas não impede movimento
        if player_is_hurt:
            player_hurt_anim_timer += 1
            if player_hurt_anim_timer >= player_hurt_anim_speed:
                player_hurt_anim_index += 1
                player_hurt_anim_timer = 0
            if player_hurt_anim_index >= 6:
                player_is_hurt = False
                player_hurt_anim_index = 0
                player_hurt_anim_timer = 0

        if player_hit_cooldown > 0:
            player_hit_cooldown -= 1

        # Movimento do jogador
        moving = False
        if keyboard.a:
            player.x -= player_speed
            moving = True
            player_facing_left = True
        if keyboard.d:
            player.x += player_speed
            moving = True
            player_facing_left = False
        if keyboard.w:
            player.y -= player_speed
            moving = True
        if keyboard.s:
            player.y += player_speed
            moving = True

        if moving != player_is_moving and not player_is_attacking:
            player_anim_index = 0
            player_anim_timer = 0
        player_is_moving = moving

        # Animação de ataque do jogador
        if player_is_attacking:
            frames = ATTACK_FRAMES_E if player_facing_left else ATTACK_FRAMES
            player_attack_timer += 1
            if player_attack_timer >= attack_anim_speed:
                player_anim_index += 1
                player_attack_timer = 0
                if player_anim_index >= len(frames):
                    player_is_attacking = False
                    player_anim_index = 0
                    for o in orcs:
                        o.already_hit = False
        else:
            # Animação de andar/parado do jogador
            if player_is_moving:
                frames = WALK_FRAMES_E if player_facing_left else WALK_FRAMES
            else:
                frames = IDLE_FRAMES_E if player_facing_left else IDLE_FRAMES
            player_anim_timer += 1
            if player_anim_timer >= player_anim_speed:
                player_anim_index = (player_anim_index + 1) % len(frames)
                player_anim_timer = 0

        for orc in orcs:
            orc.update(player)

        # Mata os orcs
        if player_is_attacking:
            for orc in orcs:
                if not orc.is_dead and not orc.already_hit:
                    dist = math.hypot(orc.x - player.x, orc.y - player.y)
                    if dist < MELEE_RANGE:
                        orc.is_dead = True
                        orc.death_anim_index = 0
                        orc.death_anim_timer = 0
                        orc.dead_time = 0
                        orc.blink_timer = 0
                        orc.visible = True
                        orc.already_hit = True
                        break

        # Ataque do orc no jogador
        for orc in orcs:
            if (
                not orc.is_dead
                and orc.player_in_range
                and orc.is_attacking
                and orc.attack_anim_index == 3  # ataque ocorre no meio da animação
                and player_hit_cooldown == 0
            ):
                player_life -= 1
                player_hit_cooldown = PLAYER_HIT_COOLDOWN
                sounds.player_hit.play()  # coloque um som player_hit.wav na pasta sounds
                if player_life <= 0:
                    player_life = 0
                    player_death_start()
                else:
                    # Inicia animação de dano do jogador (mas não impede movimento)
                    player_is_hurt = True
                    player_hurt_anim_index = 0
                    player_hurt_anim_timer = 0

        # Só inicia a próxima horda quando TODOS os orcs sumirem de vez
        if orcs and all(orc.is_dead and not orc.visible for orc in orcs):
            orcs.clear()
            wave_count += 1
            orcs = spawn_wave(wave_count)

def player_death_start():
    # Inicia a animação de morte do jogador
    global player_is_dead, player_death_anim_index, player_death_anim_timer, game_over_timer, player_is_attacking, player_is_hurt
    player_is_dead = True
    player_death_anim_index = 0
    player_death_anim_timer = 0
    game_over_timer = 0
    player_is_attacking = False
    player_is_hurt = False

def reset_game():
    # Reinicia todos os parâmetros do jogo
    global player, player_life, player_hit_cooldown, player_is_dead, player_death_anim_index, player_death_anim_timer, game_over_timer
    global orcs, wave_count, player_anim_index, player_anim_timer, player_is_attacking, player_attack_timer, player_is_moving, player_facing_left
    global player_is_hurt, player_hurt_anim_index, player_hurt_anim_timer
    player.x = WIDTH // 2
    player.y = HEIGHT // 2
    player_life = 3
    player_hit_cooldown = 0
    player_is_dead = False
    player_death_anim_index = 0
    player_death_anim_timer = 0
    game_over_timer = 0
    player_anim_index = 0
    player_anim_timer = 0
    player_is_attacking = False
    player_attack_timer = 0
    player_is_moving = False
    player_facing_left = False
    player_is_hurt = False
    player_hurt_anim_index = 0
    player_hurt_anim_timer = 0
    wave_count = 1
    orcs.clear()
    orcs.extend(spawn_wave(wave_count))

def on_key_down(key):
    # Permite sair para o menu com ESC
    global state
    if state == GAME and key == keys.ESCAPE:
        state = MENU
        reset_game()

def start():
    # Inicia a música se estiver ativada
    if music_on:
        music.play("background_music")

start()
pgzrun.go()