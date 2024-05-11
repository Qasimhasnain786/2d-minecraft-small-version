import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")

# Each tile size is 30 adn there are 20 tiles
tile_size = WIDTH // 20


player_img = pygame.image.load("assets/player.png")
background_img = pygame.image.load("assets/world/background.png")
dirt_img = pygame.image.load("assets/world/dirt.png")
grass_img = pygame.image.load("assets/world/grass.png")
stone_img = pygame.image.load("assets/world/stone.png")
dirt_small_img = pygame.transform.scale(
    pygame.image.load("assets/world/dirt.png"), (10, 10)
)
grass_small_img = pygame.transform.scale(
    pygame.image.load("assets/world/grass.png"), (10, 10)
)

clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.inventory = []
        self.selected_block = 0

        self.gravity = 0.5
        self.jumping = False
        self.dx = 0
        self.dy = 0

    def draw(self):
        screen.blit(self.image, self.rect)
        if self.selected_block != 0:
            if self.selected_block == 1:
                screen.blit(dirt_small_img, (self.rect.right - 5, self.rect.top + 20))
            elif self.selected_block == 2:
                screen.blit(grass_small_img, (self.rect.right - 5, self.rect.top + 20))

    def controls(self):
        self.dx = 0
        if self.keys[K_a]:
            self.dx = -5
        if self.keys[K_d]:
            self.dx = 5
        if self.keys[K_w] and not self.jumping:
            self.dy = -9
            self.jumping = True
        if not self.keys[K_w]:
            self.jumping = False
        if self.keys[K_e]:
            print(self.inventory, flush=1)
        # if pygame.mouse.get_pressed()[2]:
        #     print("yes")

    def collision(self):
        global world_data
        for tile in tile_list:
            if tile[1] == 1 or tile[1] == 2 or tile[1] == 3:
                if tile[2].colliderect(
                    self.rect.x + self.dx,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height,
                ):
                    self.dx = 0
                if tile[2].colliderect(
                    self.rect.x,
                    self.rect.y + self.dy,
                    self.rect.width,
                    self.rect.height,
                ):
                    self.dy = 0

    def break_block(self):
        for tile in tile_list:
            if tile[1] == 1 or tile[1] == 2:
                if tile[2].colliderect(
                    (
                        self.rect.left + 20,
                        self.rect.y,
                        self.rect.width,
                        self.rect.height,
                    )
                ) or tile[2].colliderect(
                    (
                        self.rect.left - 20,
                        self.rect.y,
                        self.rect.width,
                        self.rect.height,
                    )
                ):
                    if (
                        tile[2].collidepoint(self.pos[0], self.pos[1])
                        and pygame.mouse.get_pressed()[0]
                    ):
                        world_data[tile[0][0]][tile[0][1]] = 0
                        self.inventory.append(tile[1])
                if tile[2].colliderect(
                    (self.rect.x, self.rect.y + 20, self.rect.width, self.rect.height)
                ) or tile[2].colliderect(
                    (self.rect.x, self.rect.y - 20, self.rect.width, self.rect.height)
                ):
                    if (
                        tile[2].collidepoint(self.pos[0], self.pos[1])
                        and pygame.mouse.get_pressed()[0]
                    ):
                        world_data[tile[0][0]][tile[0][1]] = 0
                        self.inventory.append(tile[1])

    def select_block(self):
        if self.keys[K_0]:
            self.selected_block = 0
        if self.keys[K_1] and 1 in self.inventory:
            self.selected_block = 1
        if self.keys[K_2] and 2 in self.inventory:
            self.selected_block = 2

        if self.selected_block == 1 and 1 not in self.inventory:
            self.selected_block = 0
        if self.selected_block == 2 and 2 not in self.inventory:
            self.selected_block = 0

    def place_block(self):
        for tile in tile_list:
            if tile[2].colliderect(
                (self.rect.left + 20, self.rect.y, self.rect.width, self.rect.height)
            ) or tile[2].colliderect(
                (self.rect.left - 20, self.rect.y, self.rect.width, self.rect.height)
            ):
                if (
                    tile[2].collidepoint(self.pos[0], self.pos[1])
                    and pygame.mouse.get_pressed()[2]
                    and self.selected_block in self.inventory
                    and tile[1] == 0
                ):
                    if not self.rect.collidepoint(self.pos[0], self.pos[1]):
                        world_data[tile[0][0]][tile[0][1]] = self.selected_block
                        self.inventory.remove(self.selected_block)
            if tile[2].colliderect(
                (self.rect.x, self.rect.y + 20, self.rect.width, self.rect.height)
            ) or tile[2].colliderect(
                (self.rect.x, self.rect.y - 20, self.rect.width, self.rect.height)
            ):
                if (
                    tile[2].collidepoint(self.pos[0], self.pos[1])
                    and pygame.mouse.get_pressed()[2]
                    and self.selected_block in self.inventory
                    and tile[1] == 0
                ):
                    if not self.rect.collidepoint(self.pos[0], self.pos[1]):
                        world_data[tile[0][0]][tile[0][1]] = self.selected_block
                        self.inventory.remove(self.selected_block)

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        self.controls()
        self.select_block()
        self.dy += self.gravity * 2
        self.collision()
        self.break_block()
        self.place_block()

        self.rect.x += self.dx
        self.rect.y += self.dy


world_data = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


def make_world(data):
    global tile_list, tile_list_done
    tile_list = []
    for row_num, row in enumerate(data):
        for col_num, colum in enumerate(row):
            if colum == 1:
                screen.blit(dirt_img, (col_num * tile_size, row_num * tile_size))
            elif colum == 2:
                screen.blit(grass_img, (col_num * tile_size, row_num * tile_size))
            elif colum == 3:
                screen.blit(stone_img, (col_num * tile_size, row_num * tile_size))
            tile_list.append(
                (
                    (row_num, col_num),
                    colum,
                    pygame.Rect(
                        col_num * tile_size,
                        row_num * tile_size,
                        tile_size,
                        tile_size,
                    ),
                )
            )


player = Player(tile_size * 2, HEIGHT - tile_size * 5)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    screen.fill("black")
    # screen.blit(background_img, (0, 0))
    make_world(world_data)
    player.draw()

    player.update()

    pygame.display.flip()
