import pygame, sys, time
from settings import *
from surfacemaker import SurfaceMaker
from sprites import Player, Ball, Block, Upgrade, Projectile
from random import choice
 
class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout')

        # background
        self.bg = self.create_bg()

        # sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites, self.surfacemaker)
        self.stage_setup()
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)

        # hearts
        self.heart_surf = pygame.image.load("graphics/other/heart.png").convert_alpha()

        # projectile
        self.projectile_surf = pygame.image.load("graphics/other/projectile.png").convert_alpha()
        self.can_shoot = True
        self.shoot_time = 0

    def create_upgrade(self, pos):
        upgrade_type = "laser" #choice(UPGRADES)
        Upgrade(pos, upgrade_type, [self.all_sprites, self.upgrade_sprites])

    def create_bg(self):
        bg_original = pygame.image.load("graphics/other/bg.png").convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        scaled_width = bg_original.get_width() * scale_factor
        scaled_height = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
        return scaled_bg
    
    def stage_setup(self):
        # cycle through all rows and columns of BLOCK_MAP
        for row_index, row in enumerate(BLOCK_MAP):
            for col_index, col in enumerate(row):
                if col != " ":
                    # fin the x and y position for each individual block
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = TOP_OFFSET + row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(col, (x, y), [self.all_sprites, self.block_sprites], self.surfacemaker, self.create_upgrade)

    def display_hearts(self):
        for i in range(self.player.hearts):
            x = 2 + i * (self.heart_surf.get_width() + 2)
            self.display_surface.blit(self.heart_surf, (x, 4))

    def upgrade_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)

    def create_projectile(self):
        for projectile in self.player.laser_rects:
            Projectile(
                projectile.midtop - pygame.math.Vector2(0, 30), 
                self.projectile_surf, 
                [self.all_sprites, self.projectile_sprites])
            
    def laser_timer(self):
        if pygame.time.get_ticks() -  self.shoot_time >= 500:
            self.can_shoot = True

    def projectile_block_collision(self):
        for projectile in self.projectile_sprites:
            overlap_sprites = pygame.sprite.spritecollide(projectile, self.block_sprites, False)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.get_damage(1)
                projectile.kill()

    def run(self):
        last_time = time.time()
        while True:
            
            # delta time
            dt = time.time() - last_time
            last_time = time.time()
 
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True
                        if self.can_shoot:
                            self.create_projectile()
                            self.can_shoot = False
                            self.shoot_time = pygame.time.get_ticks()

            # draw background
            self.display_surface.blit(self.bg, (0, 0))

            # update the game
            self.all_sprites.update(dt)
            self.upgrade_collision()
            self.laser_timer()
            self.projectile_block_collision( )

            # draw the frame
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()
 
            # update window
            pygame.display.update()
 
if __name__ == '__main__':
    game = Game()
    game.run()
 
