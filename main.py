import pygame, sys, random
pygame.init()
pygame.font.init()
pygame.mixer.init()


HIT_SOUND = pygame.mixer.Sound("assets/audio/hit.mp3")
WING_SOUND = pygame.mixer.Sound("assets/audio/wing.mp3")
SCORE_FONT = pygame.font.SysFont("comicsans", 60)
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.4
BIRD_WIDTH, BIRD_HEIGHT = 68, 48    
WIDTH, HEIGHT = 576, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quan is learning to make flappy bird")
#background 
bg_surface = pygame.transform.scale(pygame.image.load("assets/sprites/background-day.png"), (WIDTH, HEIGHT))
lobby_surface = pygame.transform.scale(pygame.image.load("assets/sprites/message.png"), (WIDTH/1.5, HEIGHT/1.8))
gameover_surface = pygame.transform.scale(pygame.image.load("assets/sprites/gameover.png"), (400, 100)) #(192, 42)
#floor 
FLOOR_HEIGHT = 150
floor_surface = pygame.transform.scale(pygame.image.load("assets/sprites/base.png").convert(), (WIDTH , FLOOR_HEIGHT))
#bird 68x48
bird_surface_midflap = pygame.transform.scale(pygame.image.load("assets/sprites/bluebird-midflap.png").convert(),(BIRD_WIDTH, BIRD_HEIGHT))
bird_surface_upflap = pygame.transform.scale(pygame.image.load("assets/sprites/bluebird-upflap.png").convert(),(BIRD_WIDTH, BIRD_HEIGHT))
bird_surface_downlap = pygame.transform.scale(pygame.image.load("assets/sprites/bluebird-downflap.png").convert(),(BIRD_WIDTH, BIRD_HEIGHT))
bird_frames = [bird_surface_midflap, bird_surface_downlap, bird_surface_upflap]
BIRD_FLAP = pygame.USEREVENT + 2
#pipes (100, 600)
PIPE_WIDTH, PIPE_HEIGHT = 100, 600
bottom_pipe_surface = pygame.transform.scale(pygame.image.load("assets/sprites/pipe-green.png").convert(), (100, 600))
top_pipe_surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/sprites/pipe-green.png").convert(), (100, 600)), 180) 
SPAWN_PIPE = pygame.USEREVENT + 1
progress = [0]



def handle_pipes_movement(top_pipes, bottom_pipes, top_pipes_fake):
    for pipe in top_pipes:
        pipe.x -= 3
    for pipe in bottom_pipes:  
        pipe.x -= 3
    for pipe in top_pipes_fake:
        pipe.x -= 3
        
def handle_floor(floor_x_pos):
    floor_x_pos -= 3
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0
    return floor_x_pos 

def collision(bird, top_pipes, bottom_pipes):
    if bird.y >= HEIGHT - FLOOR_HEIGHT:
        HIT_SOUND.play()
        return False

    for pipe in top_pipes:
        if pipe.colliderect(bird):
            HIT_SOUND.play()
            return False
    for pipe in bottom_pipes:
        if pipe.colliderect(bird):
            HIT_SOUND.play()
            return False
    else: 
        return True

def draw_lobby(bird):
    WIN.blit(bg_surface, (0, 0))
    WIN.blit(lobby_surface, (WIDTH/2 - lobby_surface.get_width()/2 , HEIGHT/2 - lobby_surface.get_height()/2))
    WIN.blit(floor_surface, (0, HEIGHT - FLOOR_HEIGHT))
    #WIN.blit(bird_surface, (bird.x, bird.y))
    max = progress[0] 
    for num in progress:
        if num > max:
            max = num 
    highest_text = SCORE_FONT.render(f"HIGHEST: {max}", 1, WHITE)
    WIN.blit(highest_text, (WIDTH/2 - highest_text.get_width()/2, 100))
    
    pygame.display.update()
    
    
    
def draw(floor_x_pos,bird, top_pipes, bottom_pipes, score, top_pipes_fake, bird_movement, bird_surface, gameover, progress): 
    WIN.blit(bg_surface, (0, 0))
    #pipe
    for pipe in top_pipes:
        WIN.blit(top_pipe_surface, (pipe.x, pipe.y))
    for pipe in bottom_pipes:
        WIN.blit(bottom_pipe_surface, (pipe.x, pipe.y))
    for pipe in top_pipes_fake:
        WIN.blit(top_pipe_surface, (pipe.x, pipe.y))
    
    #floor
    WIN.blit(floor_surface, (floor_x_pos, HEIGHT - FLOOR_HEIGHT))
    WIN.blit(floor_surface, (floor_x_pos + WIDTH, HEIGHT - FLOOR_HEIGHT))
    #score 
    score_text = SCORE_FONT.render(str(score), 1, WHITE) 
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 100))
    #bird
    rotated_bird = pygame.transform.rotozoom(bird_surface, 1.5*bird_movement, 1)
    WIN.blit(rotated_bird, (100, bird.y))
    #gameover
    if gameover == True:
        WIN.blit(gameover_surface, (WIDTH/2 - gameover_surface.get_width()/2, HEIGHT - 150 - 100))
        max = progress[0] 
        for num in progress:
            if num > max:
                max = num 
        highest_text = SCORE_FONT.render(f"HIGHEST: {max}", 1, WHITE)
        WIN.blit(highest_text, (WIDTH/2 - highest_text.get_width()/2, 10))

    pygame.display.update()
    
def handle_score(bird, top_pipes, bottom_pipes, score):
    for pipe in top_pipes:
        if bird.x >= pipe.x + PIPE_WIDTH:
            score += 1
            top_pipes.remove(pipe)
    return score

def main():
    clock = pygame.time.Clock() 
    run = False
    floor_x_pos = 0
    bird_movement = 0
    bird = pygame.Rect(100, HEIGHT/2 - BIRD_HEIGHT/2, BIRD_WIDTH, BIRD_HEIGHT)
    pygame.time.set_timer(SPAWN_PIPE, 1200) 
    pygame.time.set_timer(BIRD_FLAP, 200)
    top_pipes = []
    bottom_pipes = []
    top_pipes_fake = []
    height = [300, 200, 180, 220, 330, 240, 230, 380, 280, 400, 350, 250, 450, 300, 200, 400, 350, 250, 450]
    score = 0 
    bird_surface_index = 2
    gameover = False
    
    while not run:
        draw_lobby(bird)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True
                

    while run:
        bird_surface = bird_frames[bird_surface_index]
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = 0 
                    bird_movement -= 10
                    WING_SOUND.play()

            if event.type == SPAWN_PIPE:
                random_height = random.choice(height)
                #top_pipes
                top_pipe = pygame.Rect(WIDTH, -random_height, PIPE_WIDTH - 10, PIPE_HEIGHT - 10)
                top_pipes.append(top_pipe)
                #bottom_pipes
                bottom_pipe = pygame.Rect(WIDTH, HEIGHT - (HEIGHT - (PIPE_HEIGHT - random_height) - 300), PIPE_WIDTH - 10, PIPE_HEIGHT - 10)
                bottom_pipes.append(bottom_pipe)
                #top_pipes_fake
                top_pipe_fake = pygame.Rect(WIDTH, -random_height, PIPE_WIDTH, PIPE_HEIGHT)
                top_pipes_fake.append(top_pipe_fake)
            
            if event.type == BIRD_FLAP:
                if bird_surface_index < 2:
                    bird_surface_index += 1
                elif bird_surface_index >= 2:
                    bird_surface_index = 0
                
        score = handle_score(bird, top_pipes, bottom_pipes, score) 
        run = collision(bird, top_pipes, bottom_pipes)
        if run == False:
            gameover = True
            progress.append(score)
            draw(floor_x_pos, bird, top_pipes, bottom_pipes, score, top_pipes_fake, bird_movement, bird_surface, gameover, progress)
            pygame.time.delay(2000)
            main()

            
        handle_pipes_movement(top_pipes, bottom_pipes, top_pipes_fake)
        floor_x_pos = handle_floor(floor_x_pos)
        
        #bird
        bird_movement += GRAVITY    
        bird.y += bird_movement
                
        draw(floor_x_pos, bird, top_pipes, bottom_pipes, score, top_pipes_fake, bird_movement, bird_surface, gameover, progress) 


   
                
if __name__ == "__main__":
    main()