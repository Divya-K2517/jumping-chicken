import pygame
import sys
import random 

pygame.init()
WIDTH, HEIGHT = 500, 600
BASE_SPEED = 2
game_speed = BASE_SPEED
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("jumping chicken")
clock = pygame.time.Clock()
running = True
game_over = False

class Chicken ():
    def __init__(self):
        self.image = pygame.image.load("jumping chicken/chicken.png")
        self.image = pygame.transform.scale(self.image, (70,70))
        self.image2 = pygame.image.load("jumping chicken/leftchicken.png")
        self.image2 = pygame.transform.scale(self.image2, (70,70))
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.rect.left = WIDTH/2
        self.jumping = False
        self.jvelocity = 0
        self.gravity = 1.2
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font("T-rex game/font.ttf", 15)
        self.facing_right = True
    def draw(self):
        if self.facing_right:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image2,self.rect)
        score_text = self.font.render("Score: " + str(int(self.score)), True, (0,0,0))
        screen.blit(score_text, (WIDTH-130, 20))
        high_score_text = self.font.render("High score: " + str(int(self.high_score)), True, (0,0,0))
        screen.blit(high_score_text, (WIDTH-130, 0))
    def update(self):
        global game_over
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.rect.left > 0:
                    self.rect.left -= 5
                    self.facing_right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.rect.right < WIDTH:
                    self.rect.right += 5
                    self.facing_right = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.jumping = True
                self.jvelocity = 15
            if self.rect.top < 0: #so the chicken doesnt go off the top edge of the screen
                self.rect.top = 0
            #when jumping
            if self.jumping:
                self.rect.bottom -= self.jvelocity
                self.jvelocity -= self.gravity
    def reset(self):
        self.rect.bottom = HEIGHT
        self.rect.left = WIDTH/2
        self.jumping = False
        self.jvelocity = 0
            
class Platform(pygame.sprite.Sprite):
    def __init__(self, x,w):
        super().__init__()
        self.image = pygame.Surface((w,15))
        self.image.fill((17,90,44))
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.landed_on = False
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def update(self):
        global game_speed
        if self.rect.bottom > HEIGHT - 20:
            if abs(chicken.rect.bottom - self.rect.top) < 10:
                global game_over
                game_over = True
        self.rect.bottom += game_speed
        if self.rect.bottom > HEIGHT:
            self.kill()
        
def checkcollision(p,c):
    landing_tolerance = 7
    if p.rect.top - landing_tolerance <= c.rect.bottom <= p.rect.top + landing_tolerance and c.rect.right >= p.rect.left and c.rect.left <= p.rect.right:
        print("collision detected")
        c.rect.bottom = p.rect.top
        c.velocity =0
        c.jumping = False
        if not p.landed_on:
            c.score += 1
            if c.score > c.high_score:
                c.high_score += 1
            p.landed_on = True

def game_over_screen():
    font = pygame.font.Font("jumping chicken/font.ttf", 40)
    text = font.render("GAME OVER", True, (255,0,0))
    screen.blit(text, (WIDTH/4, HEIGHT/3))
    restart_font = pygame.font.Font("jumping chicken/font.ttf", 20)
    restart_text = restart_font.render("press "+ "'r'" + " to restart game", True, (255,0,0))
    screen.blit (restart_text,(WIDTH/5, HEIGHT/3 + 50))
    chicken.rect.bottom = HEIGHT
    global game_over 
    game_over = True

def spawn_platform():
    new_platform = Platform(random.randint(0,WIDTH-int(WIDTH/4)), random.randint(chicken.rect.width,int(WIDTH/5)))
    while pygame.sprite.spritecollideany(new_platform, platforms):
        new_platform = Platform(random.randint(0,WIDTH-int(WIDTH/4)), random.randint(chicken.rect.width,int(WIDTH/5)))
    platforms.add(new_platform)

#objects
chicken = Chicken()
platforms = pygame.sprite.Group()
platform = Platform(random.randint(0,WIDTH-int(WIDTH/4)), random.randint(chicken.rect.width,int(WIDTH/3)))
platforms.add(platform)

#main loop
while running:
    dt = clock.tick(60)/1000  #time passed since last frame
    #so the user can close the game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill((203,245,255))
    #game code
    chicken.draw()
    chicken.update()
    #spawning new platforms
    if not game_over:
        if len(platforms) < 3:
            if len(platforms) == 0:
                spawn_platform()
            else:
                highest_p = min(platforms, key=lambda p: p.rect.top).rect.top
                highest_p -= 20
                if highest_p >= HEIGHT/4:
                    spawn_platform()
                
    platforms.draw(screen)
    platforms.update()

    for p in platforms:
        checkcollision(p, chicken)

    game_speed += 0.008

    if chicken.rect.bottom > HEIGHT or game_over:
        game_over_screen()
    
    #resetting game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        game_speed = BASE_SPEED
        platforms.empty()
        game_over = False
        chicken.reset()
        chicken.score = 0
        chicken.facing_right = True
        platforms.add(Platform(random.randint(0,WIDTH-int(WIDTH/4)), random.randint(chicken.rect.width,int(WIDTH/4))))
        

    pygame.display.flip() #updates display

#quites pygame and closes the window
pygame.quit()
sys.exit()