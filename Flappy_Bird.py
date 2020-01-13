import random
import pygame

# Creating a starting and ending menu as well as difficulty selection system

pygame.init()

# Set Window Size
screen = pygame.display.set_mode((800, 600))
# Set Window Title
pygame.display.set_caption('Flappy Bird')

BirdImg = pygame.image.load('smirk.png')
Background = pygame.image.load('Background.png')
Upper_pipe = pygame.image.load('upper_pipe.png')
Lower_pipe = pygame.image.load('lower_pipe.png')

pipe_pos = 800
upper = random.randint(150,231)
distance = random.randint(150,250)
lower = upper + distance
scores = 0

class Bird(object):
# To increase game performance, the detection of collision should be run seperate
# to the moving of the Flappy Bird, through multitheading.

    def __init__(self, x, y, sy):
        self.x = x
        self.y = y
        self.sy = sy
        self.is_alive = True

    def move(self, screen):
        self.y += self.sy
        self.sy += 1

    def accelerate(self, screen):
        self.sy -= 5

    def show(self, screen):
         # pygame.draw.circle(screen,(255,255,0),(self.x,self.y),30,0)
         screen.blit(BirdImg, (self.x, self.y))
         # Rect (x.start_point, y.start_point, x.length, y.length)
         global pipe_pos
         global upper
         global distance
         global lower
         # Don't actually need lower, can do this by randoming the distance between the two pipes between 150,300, and filling the lower part
         rect1 = pygame.Rect(pipe_pos+10,0,40,upper)
         rect2 = pygame.Rect(pipe_pos+10,lower,40,600 - lower)
         pygame.draw.rect(screen, (0,255,0), rect1, 0)
         pygame.draw.rect(screen, (0,255,0), rect2, 0)
         screen.blit(Upper_pipe,[pipe_pos,upper-220])
         screen.blit(Lower_pipe,[pipe_pos,upper-400])
         screen.blit(Lower_pipe,[pipe_pos,lower-10])
         screen.blit(Upper_pipe,[pipe_pos,lower+200])
         pipe_pos -= 10

    def border_collision_check(self):
        global pipe_pos, scores
        if (self.y > 600 or self.y < 0) and self.is_alive == True:
            print('You died of border!')
            print("Your scores is %d"%scores)
            self.is_alive = False

    def pipe_collision_check(self):
        global upper, lower, pipe_pos, scores
        if (pipe_pos - self.x < 30 and self.x - pipe_pos < 70) and self.is_alive == True:
            if self.y < upper or self.y > lower:
                print('You died of pipe!')
                print("Your scores is %d"%scores)
                self.is_alive = False

    def pipe_check(self):
        global pipe_pos, upper, distance, lower, scores
        if pipe_pos < -60:
            upper = random.randint(150,275)
            distance = random.randint(150,250)
            lower = upper + distance
            pipe_pos = 800
            scores += 1
            return upper, distance, lower, pipe_pos, scores

    def show_scores(self):
        global scores
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score: %d' %scores, True, (0,0,0), (255,255,255))
        textRect = text.get_rect()
        textRect.center = (75,25)
        screen.blit(text,textRect)
        
            
def main():
    # Start Main Sequence
    screen.fill((0,0,0))
    x, y = 120, 300
    sy = 5
    bird = Bird(x,y,sy)
    running = True  
    while running:
        # screen.blit(text,textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or bird.is_alive == False:
                running = False
            # Initialization of Bird
            screen.blit(Background,[0,0])
            bird.show(screen)
            bird.move(screen)
            bird.border_collision_check()
            bird.pipe_collision_check()
            bird.pipe_check()
            bird.show_scores()
            # Mouse Control: starting of game
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird.accelerate(screen)
        # bird.show(screen)
        pygame.display.flip() 
        pygame.time.delay(20)

    # quiting the program after running is over
    pygame.quit()


if __name__ == '__main__':
    main()
