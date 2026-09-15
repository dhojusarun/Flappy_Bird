
import pygame
import random
import sys

# ============================================
# INITIALIZATION
# ============================================

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60


# ============================================
# COLORS
# ============================================

SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GREEN = (50, 180, 70)
DARK_GREEN = (30, 120, 40)
RED = (220, 50, 50)
BROWN = (180, 120, 60)


# ============================================
# FONTS
# ============================================

font = pygame.font.Font(None, 45)
small_font = pygame.font.Font(None, 35)
big_font = pygame.font.Font(None, 80)


# ============================================
# BIRD SETTINGS
# ============================================

BIRD_X = 150
BIRD_WIDTH = 40
BIRD_HEIGHT = 30

bird_y = HEIGHT // 2
bird_velocity = 0

GRAVITY = 0.5
JUMP_STRENGTH = -9

bird = pygame.Rect(
    BIRD_X,
    bird_y,
    BIRD_WIDTH,
    BIRD_HEIGHT
)


# ============================================
# PIPE SETTINGS
# ============================================

PIPE_WIDTH = 80
PIPE_GAP = 180
PIPE_SPEED = 4


# ============================================
# GAME VARIABLES
# ============================================

pipes = []

score = 0
high_score = 0

game_started = False
game_over = False


# ============================================
# CREATE PIPE
# ============================================

def create_pipe(x):

    gap_center = random.randint(
        180,
        HEIGHT - 180
    )

    top_height = gap_center - PIPE_GAP // 2
    bottom_y = gap_center + PIPE_GAP // 2

    top_pipe = pygame.Rect(
        x,
        0,
        PIPE_WIDTH,
        top_height
    )

    bottom_pipe = pygame.Rect(
        x,
        bottom_y,
        PIPE_WIDTH,
        HEIGHT - bottom_y
    )

    return {
        "top": top_pipe,
        "bottom": bottom_pipe,
        "passed": False
    }


# ============================================
# RESET GAME
# ============================================

def reset_game():

    global bird_y
    global bird_velocity
    global pipes
    global score
    global game_started
    global game_over

    bird_y = HEIGHT // 2
    bird_velocity = 0

    bird.y = int(bird_y)

    pipes = [
        create_pipe(500),
        create_pipe(850),
        create_pipe(1200)
    ]

    score = 0

    game_started = False
    game_over = False


# ============================================
# DRAW BIRD
# ============================================

def draw_bird():

    # Body
    pygame.draw.ellipse(
        screen,
        YELLOW,
        bird
    )

    # Wing
    wing = pygame.Rect(
        bird.x + 5,
        bird.y + 15,
        20,
        10
    )

    pygame.draw.ellipse(
        screen,
        ORANGE,
        wing
    )

    # Eye
    pygame.draw.circle(
        screen,
        WHITE,
        (bird.x + 29, bird.y + 8),
        6
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (bird.x + 31, bird.y + 8),
        3
    )

    # Beak
    pygame.draw.polygon(
        screen,
        ORANGE,
        [
            (bird.right - 2, bird.y + 10),
            (bird.right + 15, bird.y + 17),
            (bird.right - 2, bird.y + 23)
        ]
    )


# ============================================
# DRAW PIPE
# ============================================

def draw_pipe(pipe):

    top = pipe["top"]
    bottom = pipe["bottom"]

    # Main pipes
    pygame.draw.rect(
        screen,
        GREEN,
        top
    )

    pygame.draw.rect(
        screen,
        GREEN,
        bottom
    )

    # Dark borders
    pygame.draw.rect(
        screen,
        DARK_GREEN,
        top,
        4
    )

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        bottom,
        4
    )

    # Pipe caps
    top_cap = pygame.Rect(
        top.x - 5,
        top.bottom - 25,
        PIPE_WIDTH + 10,
        25
    )

    bottom_cap = pygame.Rect(
        bottom.x - 5,
        bottom.y,
        PIPE_WIDTH + 10,
        25
    )

    pygame.draw.rect(
        screen,
        GREEN,
        top_cap
    )

    pygame.draw.rect(
        screen,
        GREEN,
        bottom_cap
    )

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        top_cap,
        4
    )

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        bottom_cap,
        4
    )


# ============================================
# DRAW CLOUD
# ============================================

def draw_cloud(x, y):

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        25
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 30, y - 10),
        35
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 65, y),
        25
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, 65, 25)
    )


# ============================================
# DRAW GROUND
# ============================================

def draw_ground():

    ground_y = HEIGHT - 40

    pygame.draw.rect(
        screen,
        BROWN,
        (0, ground_y, WIDTH, 40)
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (0, ground_y, WIDTH, 8)
    )


# ============================================
# START GAME
# ============================================

reset_game()


# ============================================
# MAIN GAME LOOP
# ============================================

running = True

while running:

    # ========================================
    # EVENTS
    # ========================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SPACE = Jump
            if event.key == pygame.K_SPACE:

                if not game_over:

                    game_started = True
                    bird_velocity = JUMP_STRENGTH

                else:

                    reset_game()

            # R = Restart
            if event.key == pygame.K_r:

                if game_over:
                    reset_game()


    # ========================================
    # GAME UPDATE
    # ========================================

    if game_started and not game_over:

        # Gravity
        bird_velocity += GRAVITY

        bird_y += bird_velocity

        bird.y = int(bird_y)

        # Move pipes
        for pipe in pipes:

            pipe["top"].x -= PIPE_SPEED
            pipe["bottom"].x -= PIPE_SPEED

        # Add new pipe
        if pipes[-1]["top"].x < WIDTH - 300:

            new_x = pipes[-1]["top"].x + 350

            pipes.append(
                create_pipe(new_x)
            )

        # Remove old pipe
        if pipes[0]["top"].right < 0:

            pipes.pop(0)

        # ====================================
        # COLLISION WITH GROUND / SKY
        # ====================================

        if bird.top <= 0:

            game_over = True

        if bird.bottom >= HEIGHT - 40:

            game_over = True

        # ====================================
        # COLLISION WITH PIPES
        # ====================================

        for pipe in pipes:

            if bird.colliderect(pipe["top"]):

                game_over = True

            if bird.colliderect(pipe["bottom"]):

                game_over = True

        # ====================================
        # SCORE
        # ====================================

        for pipe in pipes:

            if (
                not pipe["passed"]
                and pipe["top"].right < bird.left
            ):

                pipe["passed"] = True

                score += 1

                if score > high_score:
                    high_score = score


    # ========================================
    # DRAW BACKGROUND
    # ========================================

    screen.fill(SKY_BLUE)

    # Clouds
    draw_cloud(100, 100)
    draw_cloud(500, 160)
    draw_cloud(300, 300)

    # ========================================
    # DRAW PIPES
    # ========================================

    for pipe in pipes:

        draw_pipe(pipe)

    # ========================================
    # DRAW BIRD
    # ========================================

    draw_bird()

    # ========================================
    # DRAW GROUND
    # ========================================

    draw_ground()

    # ========================================
    # SCORE
    # ========================================

    score_text = font.render(
        str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 -
            score_text.get_width() // 2,
            40
        )
    )

    # ========================================
    # START SCREEN
    # ========================================

    if not game_started and not game_over:

        title = big_font.render(
            "FLAPPY BIRD",
            True,
            YELLOW
        )

        instruction = small_font.render(
            "Press SPACE to Fly",
            True,
            BLACK
        )

        screen.blit(
            title,
            (
                WIDTH // 2 -
                title.get_width() // 2,
                200
            )
        )

        screen.blit(
            instruction,
            (
                WIDTH // 2 -
                instruction.get_width() // 2,
                290
            )
        )

    # ========================================
    # GAME OVER SCREEN
    # ========================================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(100)
        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        final_score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        high_score_text = font.render(
            f"High Score: {high_score}",
            True,
            YELLOW
        )

        restart_text = small_font.render(
            "Press SPACE or R to Restart",
            True,
            WHITE
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 -
                game_over_text.get_width() // 2,
                190
            )
        )

        screen.blit(
            final_score_text,
            (
                WIDTH // 2 -
                final_score_text.get_width() // 2,
                290
            )
        )

        screen.blit(
            high_score_text,
            (
                WIDTH // 2 -
                high_score_text.get_width() // 2,
                335
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                400
            )
        )

    # ========================================
    # UPDATE SCREEN
    # ========================================

    pygame.display.update()

    clock.tick(FPS)


# ============================================
# EXIT
# ============================================

pygame.quit()
sys.exit()
