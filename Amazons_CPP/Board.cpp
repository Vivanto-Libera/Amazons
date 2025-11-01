#include "Board.h"

using S = Board::State;

const int Board::rowDirection[8]{ -1, -1, 0, 1, 1, 1, 0, -1 };
const int Board::colDirection[8]{ 0, 1, 1, 1, 0, -1, -1, -1 };

S Board::isTerminal()
{
	int amazons[4];
	if (turn == S::BLACK)
	{
		amazons[0] = blackAmazons[0];
		amazons[1] = blackAmazons[1];
		amazons[2] = blackAmazons[2];
		amazons[3] = blackAmazons[3];
	}
	else
	{
		amazons[0] = whiteAmazons[0];
		amazons[1] = whiteAmazons[1];
		amazons[2] = whiteAmazons[2];
		amazons[3] = whiteAmazons[3];
	}
	for (int a = 0; a < 4; a++)
	{
		int amazon = amazons[a];
		std::array<int, 2> rowAndCol = indextoLocation(amazon);
		int row = rowAndCol[0];
		int col = rowAndCol[1];
		for (int i = 0; i < 8; i++)
		{
			int newRow = row + Board::rowDirection[i];
			int newCol = col + Board::colDirection[i];
			if (newRow < 0 || newRow > 9 || newCol < 0 || newCol > 9)
			{
				continue;
			}
			if (board[newRow][newCol] == S::EMPTY)
			{
				return S::EMPTY;
			}
		}
	}
	if (turn == S::BLACK)
	{
		return S::WHITE;
	}
	else
	{
		return S::BLACK;
	}
}
std::vector<int> Board::legalMoves()
{
	std::vector<int> moves;
	int amazons[4];
	if (turn == S::BLACK)
	{
		amazons[0] = blackAmazons[0];
		amazons[1] = blackAmazons[1];
		amazons[2] = blackAmazons[2];
		amazons[3] = blackAmazons[3];
	}
	else
	{
		amazons[0] = whiteAmazons[0];
		amazons[1] = whiteAmazons[1];
		amazons[2] = whiteAmazons[2];
		amazons[3] = whiteAmazons[3];
	}
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 8; j++)
		{
			std::array<int, 2> rowAndCol = indextoLocation(amazons[i]);
			int row = rowAndCol[0];
			int col = rowAndCol[1];
			while (true)
			{
				row += rowDirection[j];
				col += colDirection[j];
				if (row < 0 || row > 9 || col < 0 || col > 9)
				{
					break;
				}
				if (board[row][col] == S::EMPTY)
				{
					std::vector<std::array<int, 2>> arrs = arrows(rowAndCol[0],rowAndCol[1], row, col);
					for (auto arr : arrs)
					{
						moves.push_back(moveToIndex(rowAndCol[0], rowAndCol[1], row, col, arr[0], arr[1]));
					}
				}
				else
				{
					break;
				}
			}
		}
	}
	return moves;
}
std::vector<std::array<int, 2>> Board::arrows(int amazonX, int amazonY, int row, int col)
{
	std::vector<std::array<int, 2>> arrs;
	S newBoard[10][10];
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			newBoard[i][j] = board[i][j];
		}
	}
	newBoard[amazonX][amazonY] = S::EMPTY;
	for (int i = 0; i < 8; i++)
	{
		int newRow = row;
		int newCol = col;
		while (true)
		{
			newRow += rowDirection[i];
			newCol += colDirection[i];
			if (newRow < 0 || newRow > 9 || newCol < 0 || newCol > 9)
			{
				break;
			}
			if (newBoard[newRow][newCol] == S::EMPTY)
			{
				std::array<int, 2> newMove = { newRow, newCol };
				arrs.push_back(newMove);
			}
			else
			{
				break;
			}
		}
	}
	return arrs;
}
void Board::applyMove(int index)
{
	std::array<int, 6> moveNums = indexToMove(index);
	int amazonRow = moveNums[0];
	int amazonCol = moveNums[1];
	int row = moveNums[2];
	int col = moveNums[3];
	board[row][col] = turn;
	int amaIndex = locationToIndex(amazonRow, amazonCol);
	if (turn == S::WHITE)
	{
		int amazon;
		for (int  i = 0; i < 4; i++)
		{
			int a = whiteAmazons[i];
			if (a == amaIndex)
			{
				amazon = i;
				break;
			}
		}
		whiteAmazons[amazon] = locationToIndex(row, col);
		turn = S::BLACK;
	}
	else
	{
		int amazon;
		for (int i = 0; i < 4; i++)
		{
			int a = blackAmazons[i];
			if (a == amaIndex)
			{
				amazon = i;
				break;
			}
		}
		blackAmazons[amazon] = locationToIndex(row, col);
		turn = S::WHITE;
	}
	board[amazonRow][amazonCol] = S::EMPTY;
	int arrRow = moveNums[4];
	int arrCol = moveNums[5];
	board[arrRow][arrCol] = S::ARROW;
}
py::tuple Board::neuralworkInput()
{
	std::array<std::array<int, 10>,10> whitePos;
	std::array<std::array<int, 10>, 10 > blackPos;
	std::array<std::array<int, 10>, 10 > arrowsPos;
	std::array<std::array<int, 10>, 10 > turnColor;
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			switch (board[i][j])
			{
				case S::EMPTY:
					whitePos[i][j] = 0;
					blackPos[i][j] = 0;
					arrowsPos[i][j] = 0;
					break;
				case S::WHITE:
					whitePos[i][j] = 1;
					blackPos[i][j] = 0;
					arrowsPos[i][j] = 0;
					break;
				case S::BLACK:
					whitePos[i][j] = 0;
					blackPos[i][j] = 1;
					arrowsPos[i][j] = 0;
					break;
				case S::ARROW:
					whitePos[i][j] = 0;
					blackPos[i][j] = 0;
					arrowsPos[i][j] = 1;
					break;
			}
		}
	}
	int color = turn == S::WHITE;
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			turnColor[i][j] = color;
		}
	}
	return py::make_tuple(whitePos, blackPos, arrowsPos, turnColor);
}


Board::Board()
{
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			board[i][j] = S::EMPTY;
		}
	}
	board[0][3] = S::BLACK;
	blackAmazons[0] = locationToIndex(0, 3);
	board[0][6] = S::BLACK;
	blackAmazons[1] = locationToIndex(0, 6);
	board[3][0] = S::BLACK;
	blackAmazons[2] = locationToIndex(3, 0);
	board[3][9] = S::BLACK;
	blackAmazons[3] = locationToIndex(3, 9);
	board[6][0] = S::WHITE;
	whiteAmazons[0] = locationToIndex(6, 0);
	board[6][9] = S::WHITE;
	whiteAmazons[1] = locationToIndex(6, 9);
	board[9][3] = S::WHITE;
	whiteAmazons[2] = locationToIndex(9, 3);
	board[9][6] = S::WHITE;
	whiteAmazons[3] = locationToIndex(9, 6);

	turn = S::WHITE;
}
Board::Board(const Board& aBoard)
{
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			board[i][j] = aBoard.board[i][j];
		}
	}
	for (int i = 0; i < 4; i++)
	{
		blackAmazons[i] = aBoard.blackAmazons[i];
		whiteAmazons[i] = aBoard.whiteAmazons[i];
	}
	turn = aBoard.turn;
}

int Board::locationToIndex(int x, int y)
{
	return 10 * x + y;
}
std::array<int, 2> Board::indextoLocation(int index)
{
	std::array<int, 2> loc;
	loc[0] = index / 10;
	loc[1] = index % 10;
	return loc;
}
int Board::moveToIndex(int fromR, int fromC, int toR, int toC, int arrR, int arrC)
{
	int from = fromR * 10 + fromC;
	int to = toR * 10 + toC;
	int arr = arrR * 10 + arrC;
	return from * 10000 + to * 100 + arr;
}
std::array<int, 6> Board::indexToMove(int index)
{
	std::array<int, 6> move;
	for (int i = 5; i >= 0; i--)
	{
		move[i] = index % 10;
		index /= 10;
	}
	return move;
}
