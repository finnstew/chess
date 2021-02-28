import view, model, pygame, sys, constants
from model import MoveType

class GameController:
    def __init__(self, SCREEN):
        self.board = model.GameBoard()
        self.SCREEN = SCREEN
        self.VIEW = view.GameView(SCREEN, self.board.getPieces())
        self.VIEW.drawBoard()
        self.board.addObserver(self.VIEW)

    def tryMove(self, event):
        mouseX, mouseY = event.pos
        x = mouseX // constants.TILE_SIZE
        y = mouseY // constants.TILE_SIZE
        move = self.VIEW.selectedPiece.piece.canMove(x, y, self.board)
        if move != MoveType.INVALID:
            if move == MoveType.PROMOTION:
                self.VIEW.flipBars()
            self.board.movePiece(x, y, self.VIEW.selectedPiece.piece, move)
            self.VIEW.selectedPiece = None


        else:
            self.VIEW.abortMove()

    def handle(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.VIEW.selectPiece(event)
            self.VIEW.currentbar.tryButtons(event)
        elif event.type == pygame.MOUSEBUTTONUP and self.VIEW.selectedPiece:
            self.tryMove(event)
        elif event.type == pygame.MOUSEMOTION:
            self.VIEW.dragPiece(event)






