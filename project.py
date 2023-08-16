import pygame
import sys
import random


def main():

    pygame.init()

    screen_width = 800
    screen_height = 450
    min_distance = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Turd")
    CLOCK = pygame.time.Clock()
    pipe_collision_list = []
    pipe_collision_list_180 = []
    fart_sound = pygame.mixer.Sound("fart.wav")
    ping_sound = pygame.mixer.Sound("score.wav")

    # Load background image and turd
    bg_image = pygame.image.load("bg.png").convert()
    pipe_image = pygame.image.load("pipe.png")
    pipe_width = pipe_image.get_width()
    pipe_height = pipe_image.get_height()
    pipe_180_image = pygame.transform.rotate(pipe_image, 180)
    pipe_180_width = pipe_180_image.get_width()
    pipe_180_height = pipe_180_image.get_height()
    turd = pygame.image.load("turd.png")
    turd_copy = pygame.image.load("turd copy.png")

    # ---------------------------- Functions --------------------------- #
    def generate_random_coords():
        return [random.randint(600, screen_width), random.randint(275, 350)]

    def generate_random_coords_top_pipes():
        return [random.randint(600, screen_width), random.randint(-300, -175)]

    def distance(x1, y1, x2 ,y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def check_min_distance(x, y, list):
        for pipe in list:
            if distance(x, y, pipe[0], pipe[1]) < min_distance:
                return False
        return True

    def create_bottom_pipe():
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            coords = generate_random_coords()
            if check_min_distance(coords[0], coords[1], bottom_pipes):
                bottom_pipes.append(coords)
                return
            attempts += 1

    def create_top_pipe():
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            coords = generate_random_coords_top_pipes()
            if check_min_distance(coords[0], coords[1], top_pipes):
                top_pipes.append(coords)
                return
            attempts += 1

    def draw_bottom_pipes():
        for pipe in bottom_pipes:
            screen.blit(pipe_image, pipe)

    def draw_top_pipes():
        for pipe in top_pipes:
            screen.blit(pipe_180_image, pipe)

    def move_bottom_pipes():
        for pipe in bottom_pipes:
            pipe[0] -= scroll_speed
            pipe_rect = pygame.Rect(pipe[0], pipe[1], pipe_width, pipe_height)
            pipe_collision_list.append(pipe_rect)

    def move_top_pipes():
        for pipe in top_pipes:
            pipe[0] -= scroll_speed
            pipe_rect_180 = pygame.Rect(pipe[0], pipe[1], pipe_180_width, pipe_180_height)
            pipe_collision_list_180.append(pipe_rect_180)

    def reset_game():
        nonlocal turd_x
        nonlocal turd_y
        nonlocal score_counter
        nonlocal last_score
        nonlocal score
        screen.fill((255,255,255))
        bottom_pipes.clear()
        top_pipes.clear()
        pipe_collision_list.clear()
        pipe_collision_list_180.clear()
        last_score = score_counter
        score_counter = 0
        score = score_font.render(" ", True, (255,255,255))
        turd_x = 300
        turd_y = 100
        pygame.time.wait(2000)

    turd_y = 100
    bottom_pipes = []
    top_pipes = []
    score_counter = 0
    last_score = 0

    # --------------------- End of functions ---------------------------- #

    # Initial positions for background image
    bg_x1 = 0
    bg_x2 = bg_image.get_width()

    # Initial position for turd
    turd_x = 300
    turd_y = 100

    # Variables for jump mechanics
    jumping = False
    GRAVITY = 0.6
    JUMP_HEIGHT = 7     
    VELOCITY = JUMP_HEIGHT

    # Set the scroll speed for background
    scroll_speed = 2

    # List for storing pipes
    bottom_pipes = []
    top_pipes = []

    # Fonts
    font = pygame.font.Font("freesansbold.ttf", 22)
    text = font.render("Press Space Key to Jump", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, screen_height / 2)

    title_font = pygame.font.Font("freesansbold.ttf", 100)
    title = title_font.render("FLAPPY TURD", True, (255,255,255))
    titleRect = title.get_rect()
    titleRect.center = (screen_width / 2, 50)

    score_font = pygame.font.Font("freesansbold.ttf", 50)
    score = score_font.render("0", True, (255,255,255))
    scoreRect = score.get_rect()
    scoreRect.center = (screen_width / 2, 30)

    display_score_font = pygame.font.Font("freesansbold.ttf", 100)
    ds = display_score_font.render("Score", True, (255,255,255))
    display_score_rect = ds.get_rect()
    display_score_rect.center = (325, 400)

    # Define states
    STATE_SPLASH = True
    STATE_PLAYING = False
    started = False

    # Pygame loop
    while True:
        # Handle window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                if STATE_SPLASH:
                    STATE_PLAYING = True
                    STATE_SPLASH = False
                    started = True

        # If paused then display splash screen
        if STATE_SPLASH:

            # Blit background, turd and text to screen
            screen.blit(bg_image, (bg_x1, 0))
            screen.blit(turd, (300, 100))
            screen.blit(text, textRect)
            screen.blit(title, titleRect)

            if started:
               ds = display_score_font.render(f"Score: {last_score}", True, (255,255,255))
               screen.blit(ds, display_score_rect)

        # If space key has been pressed start game
        elif STATE_PLAYING: 
            # Find out if space key is pressed
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                jumping = True 
                VELOCITY = JUMP_HEIGHT

            # Jump physics
            if jumping:
                turd_y -= VELOCITY
                VELOCITY -= GRAVITY 

            # Check if turd passed bottom pipe and increment score
            score_counter = 0
            
            for pipe in pipe_collision_list:
                if pipe[0] + pipe_width < 300:
                    score_counter += 1 
                    score = score_font.render(f"{score_counter}", True, (255,255,255))
                if 295 <= pipe[0] + pipe_width <= 300:
                    ping_sound.play()
                    
            # Collision handling
            turd_rect = turd_copy.get_rect(topleft=(turd_x,turd_y))
            turd_mask = pygame.mask.from_surface(turd)
            mask_image = turd_mask.to_surface()

            if turd_rect.collidelist(pipe_collision_list) >= 0:
                fart_sound.play()
                reset_game()
                STATE_SPLASH = True

            if turd_rect.collidelist(pipe_collision_list_180) >= 0:
                fart_sound.play()
                reset_game()
                STATE_SPLASH = True

            # If turd exits screen end game
            if turd_rect.y > screen_height:
                fart_sound.play()
                reset_game()
                STATE_SPLASH = True
                
            if turd_rect.y + turd_rect.height < 0:
                fart_sound.play()
                reset_game()
                STATE_SPLASH = True

            # Move the background images to the left
            bg_x1 -= .5
            bg_x2 -= .5

            # If the first background image has moved completely off the screen, reset its position
            if bg_x1 + bg_image.get_width() <= 0:
                bg_x1 = bg_image.get_width()

            # If the second background image has moved completely off the screen, reset its position
            if bg_x2 + bg_image.get_width() <= 0 :
                bg_x2 = bg_image.get_width()

            # Generate new bottom pipes
            if len(bottom_pipes) < 50:  # Adjust the number of objects as needed
                create_bottom_pipe()

            # Generate new top pipes
            if len(top_pipes) < 50:
                create_top_pipe()
            

            # Fill the screen with the background image
            screen.blit(bg_image, (bg_x1, 0))
            screen.blit(bg_image, (bg_x2, 0))

            # Reset lists to remove old coordinates
            pipe_collision_list_180 = []
            pipe_collision_list = []

            draw_bottom_pipes()  
            move_bottom_pipes()
            draw_top_pipes()  
            move_top_pipes()

            screen.blit(turd, (turd_x, turd_y))
            score = score_font.render(f"{score_counter}", True, (255,255,255))
            screen.blit(score, scoreRect)
            #pygame.draw.rect(screen, (255,255,255), turd_rect, 2)

        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    main() 