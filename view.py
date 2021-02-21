import pygame
from constants import TILE_SIZE, WHITE, BLACK, TILE_LENGTH, BAR_HEIGHT, font
class Tile:
   def __init__(self, color, x, y):
       self.color = BLACK if color else WHITE
       self.rect = pygame.Rect(x*TILE_SIZE,y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

   def draw(self, SCREEN):
       pygame.draw.rect(SCREEN, self.color, self.rect)



class GameView:
   def __init__(self, SCREEN, pieces):
       self.tiles = []
       self.screen = SCREEN
       self.buttons = []
       self.selectedPiece = None
       self.statusbar = StatusBar()
       for piece in pieces:
           self.buttons.append(PieceButton(piece))
       for y in range(TILE_LENGTH):
           for x in range(TILE_LENGTH):
               self.tiles.append(Tile((x+y)%2 == 0, x, y))
   def selectPiece(self, event):
       for button in self.buttons:
           if button.rect.collidepoint(event.pos):
               self.selectedPiece = button

   def dragPiece(self, event):
       if self.selectedPiece:
           mouseX, mouseY = event.pos
           self.selectedPiece.rect.x = mouseX - TILE_SIZE/2
           self.selectedPiece.rect.y = mouseY - TILE_SIZE/2
           self.drawBoard()
   def dropPiece(self, event):
       if self.selectedPiece:
           mouseX, mouseY = event.pos
           self.selectedPiece.rect.x = mouseX // TILE_SIZE * TILE_SIZE
           self.selectedPiece.rect.y = mouseY // TILE_SIZE * TILE_SIZE
           self.selectedPiece = None
           self.drawBoard()
   def drawBoard(self):
       for item in (self.tiles):
           item.draw(self.screen)
       for item in (self.buttons):
           item.draw(self.screen)
       self.statusbar.draw(self.screen)
       pygame.display.update()


   def abortMove(self):
       self.selectedPiece.rect.x = self.selectedPiece.piece.x * 100
       self.selectedPiece.rect.y = self.selectedPiece.piece.y * 100
       self.selectedPiece = None
       self.drawBoard()

   def update(self, board):
       for button in self.buttons:
           button.setLocation()

       if board.capturedPiece:
           for button in self.buttons[:]:
               if button.piece == board.capturedPiece:
                   self.buttons.remove(button)
       self.drawBoard()

class PieceButton:
   def __init__(self, piece):
       self.piece = piece
       self.rect = pygame.Rect(piece.x*TILE_SIZE, piece.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
   def draw(self, screen):
       screen.blit(self.piece.image, self.rect)

   def setLocation(self):
       self.rect.x = self.piece.x * TILE_SIZE
       self.rect.y = self.piece.y * TILE_SIZE

class StatusBar(pygame.Surface):
   def __init__(self):
       self.width = TILE_LENGTH*TILE_SIZE
       self.height = BAR_HEIGHT
       super().__init__((self.width, self.height))
       self.buttons = (Button(500, 10, None, "Draw"))

   def draw(self, surface):
       surface.blit(self, 0, TILE_SIZE*TILE_LENGTH)
       for button in self.buttons:
           button.draw(self)

class Button(pygame.Rect):
   def __init__(self, x, y, onclick, text):
       self.onclick = onclick
       self.text = font.render(text, False, (0,0,0))
       super().__init__(x, y, 140, BAR_HEIGHT - 20)


   def draw(self, surface):
       pygame.draw.rect.draw(surface, (60, 90, 190), self)
       surface.blit(self.text, self.x, self.y)

