import pygame


pygame.font.init()
font = pygame.font.SysFont('Arial', 50, bold=True)

BAR_HEIGHT = 100
TILE_SIZE = 100
TILE_LENGTH = 8
SCREEN_DIM = (TILE_SIZE*TILE_LENGTH, TILE_SIZE*TILE_LENGTH + BAR_HEIGHT)
BLACK = (50,50,50)
WHITE = (255,255,255)


pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_DIM)
WHITE_PAWN = pygame.transform.scale(pygame.image.load("resources/white_pawn.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_PAWN = pygame.transform.scale(pygame.image.load("resources/black_pawn.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
WHITE_BISHOP = pygame.transform.scale(pygame.image.load("resources/white_bishop.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_BISHOP = pygame.transform.scale(pygame.image.load("resources/black_bishop.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
WHITE_KING = pygame.transform.scale(pygame.image.load("resources/white_king.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_KING = pygame.transform.scale(pygame.image.load("resources/black_king.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load("resources/white_queen.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load("resources/black_queen.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load("resources/white_knight.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load("resources/black_knight.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
WHITE_ROOK = pygame.transform.scale(pygame.image.load("resources/white_rook.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
BLACK_ROOK = pygame.transform.scale(pygame.image.load("resources/black_rook.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

