import pygame
from sys import exit
import random


#Set window height
width=360
height = 640

bx=width/8
by=height/2
bw=34
bh=24

px= width
py=0
pw=64
ph=512

#Initialize pygame
pygame.init()

window=pygame.display.set_mode((width,height))

pygame.display.set_caption("Flappy Bird")

clock=pygame.time.Clock()

background_image = pygame.image.load("flappybirdbg.png")
bird_image=pygame.image.load("flappybird.png")
bird_image=pygame.transform.scale(bird_image,(bw,bh))
top_pipe_image=pygame.image.load("toppipe.png")
top_pipe_image=pygame.transform.scale(top_pipe_image,(pw,ph))
bottom_pipe_image=pygame.image.load("bottompipe.png")
bottom_pipe_image=pygame.transform.scale(bottom_pipe_image,(pw,ph))

pipes=[]

class Bird(pygame.Rect):
    def __init__(self,image):
        pygame.Rect.__init__(self,bx,by,bw,bh)
        self.image=image
    
class Pipe(pygame.Rect):
    def __init__(self,image):
        pygame.Rect.__init__(self,px,py,pw,ph)
        self.image=image
        self.passed=False

bird = Bird(bird_image)
velocity_x=-2
velocity_y=0
gravity=0.4
score=0
game_over = False

def draw():
    window.blit(background_image,(0,0))
    window.blit(bird.image,bird)
    for pipe in pipes:
        window.blit(pipe.image,pipe)
    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: "+text_str
    text_font = pygame.font.SysFont("Comic Sans MS" , 45)
    text_render = text_font.render(text_str,True,"white")
    window.blit(text_render,(5,0))

def move():
    global velocity_y,score,game_over
    velocity_y+=gravity
    bird.y+=velocity_y
    bird.y = max(bird.y,0)

    if bird.y >  height:
        game_over = True
        return
    for pipe in pipes:
        pipe.x+=velocity_x
        if not pipe.passed and bird.x > pipe.x + pw:
            score += 0.5
            pipe.passed=True
        if bird.colliderect(pipe):
            game_over = True
            return
    
    while len(pipes) > 0 and pipes[0].x < -pw:
        pipes.pop(0)

def create_pipe():
    random_pipe_y = py - ph/4 - random.random() * (ph/2)
    Opening_Space = height/4

    top_pipe=Pipe(top_pipe_image)
    top_pipe.y=random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe=Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + Opening_Space
    pipes.append(bottom_pipe)

    print(len(pipes))
    
create_pipe_timer=pygame.USEREVENT + 0
pygame.time.set_timer(create_pipe_timer,1500)

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == create_pipe_timer and not game_over:
            create_pipe()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w,pygame.K_SPACE,pygame.K_UP):
                velocity_y = -6
                if game_over:
                    bird.y=by
                    pipes.clear()
                    score = 0
                    game_over = False 
    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)

