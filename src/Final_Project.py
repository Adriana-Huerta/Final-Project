import random
import math
import pygame
from PIL import Image


class Particle():
    def __init__(self, pos=(0,0), size=15, life=1000):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(random.randrange(250, 255), random.randrange(0, 255), random.randrange(0, 255),255)
        self.age = 0
        self.life = life
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()


    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        self.alpha = 255 * (1 - (self.age / self.life))

    def update_surface(self):
        surf = pygame.Surface((self.size*0.8, self.size*0.8) )
        surf.fill(self.color)
        return surf
        
    def draw(self, surface):
        if self.dead:
            return 
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)
    

class ParticleTrail():
    
    def __init__(self, pos, size, life):
        self.pos = pos
        self.size = size
        self.life = life
        self.particles = []
    
    def update(self, dt):
        particle = Particle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle)
        self._update_particles(dt)
        self._update_pos()

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]
    

    def _update_pos(self):
        x, y = self.pos
        y += self.size
        self.pos = (x, y)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Rain():

    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 25
        self.birth_rate = 1
        self.trails = []
    
    def update(self, dt):
        self._birth_new_trails()
        self._update_trails(dt)

    def _update_trails(self, dt):
        for idx, trail in enumerate(self.trails):
            trail.update(dt)
            if self._trail_is_offscreen(trail):
                del self.trails[idx]
    
    def _trail_is_offscreen(self, trail):
        if not trail.particles:
            return True
        tail_is_offscreen = trail.particles[-1].pos[1] > self.screen_res[1]
        return tail_is_offscreen
    
    def _birth_new_trails(self):
        for count in range(self.birth_rate):
            screen_width = self.screen_res[0]
            x = random.randrange(0, screen_width, self.particle_size)
            pos = (x, 0)
            life = random.randrange(500, 3000)
            trail = ParticleTrail(pos, self.particle_size, life)
            self.trails.insert(0, trail)
    
    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)


class Movement():
    def __init__(self, wizardimg):
        self.wizardimg = wizardimg
        self.x = 500
        self.y = 620


    # def update(self, dt):

    # loop through the list of pygame events, and check if the keys we care about are pressed down, then change the coordinates of the wizard accordingly

    def draw(self, surface):
        #self.wizardimg
        surface.blit(self.wizardimg, (self.x,self.y))

class Fireball():
    def __init__(self, fireballimg, x):
        self.fireballimg = fireballimg
        self.x = x
        self.y = 620
        self.dead = False

    def update(self):
        self.y -= 25
        # if off screen, set dead to true
        if self.y < -375:
            self.dead = True

    def draw(self, surface):
        surface.blit(self.fireballimg, (self.x,self.y))

def main():
    pygame.init()    
    pygame.display.set_caption("Digital Rain")
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    resolution = pygame.display.get_window_size()
    print(resolution)
    rain = Rain(resolution)
    wizardimg = pygame.image.load('src/Wizard.png')
    fireballimg = pygame.image.load('src/Fire.png')
    Castle1 = pygame.image.load('src/Castle1.png')
    Castle2 = pygame.image.load('src/Castle2.png')
    wizard = Movement(wizardimg)
    fireballs = []
    running = True
    vel = 25
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fireball = Fireball(fireballimg, wizard.x)
                    fireballs.append(fireball)

        if keys[pygame.K_LEFT]:
            wizard.x -= vel
        if keys[pygame.K_RIGHT]:
            wizard.x += vel
        rain.update(dt)
        maroon = pygame.Color(25, 0, 0)
        screen.fill(maroon)
        rain.draw(screen)
        screen.blit(Castle1, (1300,620))
        screen.blit(Castle2, (0,620))

        for fireball in fireballs:
            fireball.update()
            fireball.draw(screen)
        for i, fireball in enumerate(fireballs):
            if fireball.dead:
                del fireballs[i]
        wizard.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(5)
        
    #def update(self, dt):
        #particle = Particle(self.pos, size=self.size, life=self.life)
        #self.particles.insert(0, particle)
        #self._update_particles(dt)
        #self._update_pos()

    pygame.quit()

if __name__ == "__main__":
    main()