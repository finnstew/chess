import constants
from constants import TILE_LENGTH
from enum import Enum


class MoveType(Enum):
    INVALID = 0
    NORMAL = 1
    CAPTURE = 2
    ENPASSANT = 3
    CASTLEING = 4
    PROMOTION = 5
    PREENPASSANT = 6



class GameBoard:
    def __init__(self):
        self.board = [[None]*TILE_LENGTH for i in range(TILE_LENGTH)]
        self.blackPieces = []
        self.whitePieces = []
        self.observers = []
        self.capturedPiece = None
        self.enpassantPiece = None
        self.removeEnpassant = None
        for y in range(TILE_LENGTH):
            for x in range(TILE_LENGTH):
                if y < 2 or y > 5:
                    self.board[y][x] = Piece.createPiece(x, y)
                    if self.board[y][x].team == constants.BLACK:
                        self.blackPieces.append(self.board[y][x])
                    else:
                        self.whitePieces.append(self.board[y][x])
    def getPieces(self):
        return self.whitePieces + self.blackPieces
    def hasPiece(self, x, y):
        return self.board[y][x] != None

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self)

    def transfer(self, x, y, piece):
        self.board[piece.y][piece.x] = None
        self.board[y][x] = piece
        piece.x = x
        piece.y = y

    def movePiece(self, x, y, piece, moveType):
        piece.hasMoved = True
        self.removeEnpassant = True
        if moveType == moveType.NORMAL:
            self.transfer(x, y, piece)
        if moveType == moveType.CAPTURE:
            self.capture(x, y)
            self.transfer(x, y, piece)
        if moveType == moveType.PREENPASSANT:
            self.enpassantPiece = piece
            self.transfer(x, y, piece)
            self.removeEnpassant = False
        if moveType == moveType.ENPASSANT:
            self.capture(x, y - piece.direction)
            self.transfer(x, y, piece)
        if moveType == moveType.CASTLEING:
            if abs(piece.x - x) == 4:
                self.transfer(x + 2, y, self.getPiece(x, y))
                self.transfer(x + 1, y, piece)
            elif abs(piece.x - x) == 3:
                self.transfer(x - 2, y, self.getPiece(x, y))
                self.transfer(piece.x + 2, y, piece)
        if moveType == moveType.PROMOTION:
            if self.hasEnemyPiece(x,y, piece):
                self.capture(x,y)
            self.transfer(x, y, piece)


        if self.removeEnpassant:
            self.enpassantPiece = None
        self.notifyObservers()
        self.capturedPiece = None

    def capture(self, x, y):
        self.capturedPiece = self.board[y][x]
        self.board[y][x] = None
        return self.capturedPiece

    def hasEnemyPiece(self, x, y, piece):
        return self.hasPiece(x, y) and self.board[y][x].team != piece.team
    def getDirection(self, new, old):
        if new < old:
            return -1
        elif old < new:
            return 1
        else:
            return 0
    def hasPieceBetween(self, x, y, piece):
        dirX = self.getDirection(x, piece.x)
        dirY = self.getDirection(y, piece.y)
        curX = piece.x + dirX
        curY = piece.y + dirY

        while curX != x or curY != y:
            if self.hasPiece(curX, curY):
                return True
            curX += dirX
            curY += dirY



        return False

    def validSpot(self, x, y):
        if -1 < y < 8 and -1 < x < 8:
            return True
        else:
            return False

    def getPiece(self, x, y):
        if self.validSpot(x, y):
            return self.board[y][x]
        else:
            return None


class Piece:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hasMoved = False
    def setPos(self, x, y):
        self.x = x
        self.y = y
    @staticmethod
    def createPiece(x, y):
        team = constants.BLACK if y < 4 else constants.WHITE
        if y == 1 or y == 6:
            return Pawn(x, y, team)
        elif x == 4:
            return King(x, y, team)
        elif x == 3:
            return Queen(x, y, team)
        elif x == 2 or x == 5:
            return Bishop(x, y, team)
        elif x == 1 or x == 6:
            return Knight(x, y, team)
        else:
            return Rook(x, y, team)
    def setImage(self, blackImage, whiteImage):
        if self.team == constants.BLACK:
            self.image = blackImage
        else:
            self.image = whiteImage
    def canMove(self, x, y, board):
        if board.hasPiece(x, y):
            return MoveType.INVALID
        else:
            return MoveType.NORMAL
    def basicMove(self, x, y, board):
        if board.hasEnemyPiece(x,y,self):
            return MoveType.CAPTURE
        elif board.hasPiece(x, y):
            return MoveType.INVALID
        else:
            return MoveType.NORMAL





class Pawn(Piece):
    blackImage = constants.BLACK_PAWN
    whiteImage = constants.WHITE_PAWN
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(Pawn.blackImage, Pawn.whiteImage)
        if self.team == constants.BLACK:
            self.direction = 1
        else:
            self.direction = -1
    def __repr__(self):
        return "Pawn" + " " + str(self.x) + " " + str(self.y) + " " + str(self.team)
    def canMove(self, x, y, board):
        if y == self.y + self.direction and x == self.x and not board.hasPiece(x,y):
            if y == 0 or y == 7:
                return MoveType.PROMOTION
            else:
                return MoveType.NORMAL

        elif y == self.y + 2 and x == self.x and self.direction == 1 and self.y == 1:
            return MoveType.PREENPASSANT
        elif y == self.y - 2 and x == self.x and self.direction == -1 and self.y == 6:
            return MoveType.PREENPASSANT
        elif y == self.y + self.direction and 1 == abs(self.x - x):
            if board.hasEnemyPiece(x,y,self):
                if y == 0 or y == 7:
                    return MoveType.PROMOTION
                else:
                    return MoveType.CAPTURE
            elif board.hasPiece(x, y - self.direction) and board.getPiece(x, y - self.direction) == board.enpassantPiece:
                return MoveType.ENPASSANT
            else:
                return MoveType.INVALID
        else:
            return MoveType.INVALID


class King(Piece):
    blackImage = constants.BLACK_KING
    whiteImage = constants.WHITE_KING
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(King.blackImage, King.whiteImage)
    def canMove(self, x, y, board):
        if (1 == abs(self.x - x) and abs(self.y - y) < 2) or (1 == abs(self.y - y) and abs(self.x - x) < 2):
            return self.basicMove(x, y, board)
        if (not self.hasMoved and isinstance(board.getPiece(x, y), Rook)
                and not board.getPiece(x, y).hasMoved and not board.hasPieceBetween(x, y, self)):
            return MoveType.CASTLEING
        else:
            return MoveType.INVALID


class Queen(Piece):
    blackImage = constants.BLACK_QUEEN
    whiteImage = constants.WHITE_QUEEN
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(Queen.blackImage, Queen.whiteImage)
    def canMove(self, x, y, board):
        if abs(self.x - x) == abs(self.y - y) and x != self.x and y != self.y and not board.hasPieceBetween(x, y, self):
            return self.basicMove(x, y, board)
        elif (x == self.x and y != self.y) or (y == self.y and x != self.x):
            if board.hasPieceBetween(x, y, self):
                return MoveType.INVALID
            return self.basicMove(x, y, board)
        else:
            return MoveType.INVALID


class Rook(Piece):
    blackImage = constants.BLACK_ROOK
    whiteImage = constants.WHITE_ROOK
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(Rook.blackImage, Rook.whiteImage)
    def canMove(self, x, y, board):
        if (x == self.x and y != self.y) or (y == self.y and x != self.x):
            if board.hasPieceBetween(x, y, self):
                return MoveType.INVALID
            return self.basicMove(x, y, board)
        else:
            return MoveType.INVALID


class Bishop(Piece):
    blackImage = constants.BLACK_BISHOP
    whiteImage = constants.WHITE_BISHOP
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(Bishop.blackImage, Bishop.whiteImage)
    def canMove(self, x, y, board):

        if abs(self.x - x) == abs(self.y - y) and x != self.x and y != self.y and not board.hasPieceBetween(x, y, self):
            return self.basicMove(x, y, board)
        else:
            return MoveType.INVALID

class Knight(Piece):
    blackImage = constants.BLACK_KNIGHT
    whiteImage = constants.WHITE_KNIGHT
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.setImage(Knight.blackImage, Knight.whiteImage)
    def canMove(self, x, y, board):
        if (abs(self.x - x) == 2 and abs(self.y - y) == 1) or (abs(self.y - y) == 2 and abs(self.x - x) == 1):
            return self.basicMove(x, y, board)
        else:
            return MoveType.INVALID


