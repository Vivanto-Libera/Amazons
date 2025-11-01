from Amazons import Board
import Amazons
def print_board(aBoard):
    board = aBoard.board()
    rowIndex = '9876543210'
    colIndex = 'a  b  c  d  e  f  g  h  i  j'
    for row in range(0, 10):
        print()
        print(rowIndex[row], end='  ')
        for col in range(0, 10):
            if board[row][col] == Amazons.State.EMPTY:
                print('.', end='  ')
            elif board[row][col] == Amazons.State.BLACK:
                print('b', end='  ')
            elif board[row][col] == Amazons.State.WHITE:
                print('w', end='  ')
            else:
                print('x', end='  ')
    print(f"\n   {colIndex}")

g = Board()
print_board(g)