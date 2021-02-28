import pygame
from constants import TILE_SIZE, WHITE, BLACK, TILE_LENGTH, BAR_HEIGHT, font
import constants
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

       self.createBars()

       self.drawBoard()
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
       self.currentbar.draw(self.screen)
       pygame.display.update()

   def createBars(self):
       self.statusbar = StatusBar()
       self.promotionbar = StatusBar()
       self.currentbar = self.statusbar
       self.statusbar.addButton(TextButton(670, 10, "Draw"), "draw")
       self.statusbar.addButton(TextButton(500, 10, "Forfeit"), "forfeit")
       self.promotionbar.addButton(ImageButton(580, 5, constants.BLACK_PAWN), "pawn")
       self.promotionbar.addButton(ImageButton(460, 5, constants.BLACK_KNIGHT), "knight")
       self.promotionbar.addButton(ImageButton(340, 5, constants.BLACK_QUEEN), "queen")
       self.promotionbar.addButton(ImageButton(220, 5, constants.BLACK_ROOK), "rook")
       self.promotionbar.addButton(ImageButton(100, 5, constants.BLACK_BISHOP), "bishop")

   def flipBars(self):
       if self.currentbar == self.statusbar:
           self.currentbar = self.promotionbar
       else:
           self.currentbar = self.statusbar

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
       self.buttons = {}
       self.components = {}

    def draw(self, surface):
       surface.blit(self, (0, TILE_SIZE*TILE_LENGTH))
       for key, button in self.buttons.items():
           print(button)
           button.draw(self)

    def addButton(self, newButton, name):
        self.buttons[name] = newButton

    def addComponent(self, newComponent, name):
        self.components[name] = newComponent

    def tryButtons(self, event):
        x,y = event.pos
        print(x,y)
        for key, button in self.buttons.items():
            if button.collidepoint(x,y-800):
                print(event.pos)

class Button(pygame.Rect):
   def __init__(self, x, y, component):
       self.onclick = lambda: print("CLICK!")
       self.component = component
       #self.name = self.component
       super().__init__(x, y, self.component.get_width(), self.component.get_height() + 10)


   def draw(self, surface):
       pygame.draw.rect(surface, (60, 90, 190), self)
       surface.blit(self.component, (self.x, self.y))

class ImageButton(Button):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class TextButton(Button):
    def __init__(self, x, y, text):
        text = font.render(text, False, (0,0,0))
        super().__init__(x, y, text)