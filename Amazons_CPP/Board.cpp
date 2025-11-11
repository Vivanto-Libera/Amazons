#include "Board.h"

using S = Board::State;

const int Board::rowDirection[8]{ -1, -1, 0, 1, 1, 1, 0, -1 };
const int Board::colDirection[8]{ 0, 1, 1, 1, 0, -1, -1, -1 };

S Board::isTerminal()
{
	int* amazons;
	if (turn == S::BLACK)
	{
		amazons = blackAmazons;
	}
	else
	{
		amazons = whiteAmazons;
	}
	for (int a = 0; a < 4; a++)
	{
		std::array<int, 2> rowAndCol = indextoLocation(amazons[a]);
		for (int i = 0; i < 8; i++)
		{
			int row = rowAndCol[0] + Board::rowDirection[i];
			int col = rowAndCol[1] + Board::colDirection[i];
			if (row < 0 || row > 9 || col < 0 || col > 9)
			{
				continue;
			}
			if (board[row][col] == S::EMPTY)
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
	int *amazons;
	if (turn == S::BLACK)
	{
		amazons = blackAmazons;
	}
	else
	{
		amazons = whiteAmazons;
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
					for (const auto& arr : arrs)
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
	S moveColor = board[amazonX][amazonY];
	board[amazonX][amazonY] = S::EMPTY;
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
			if (board[newRow][newCol] == S::EMPTY)
			{
				arrs.push_back(std::array<int, 2>{newRow, newCol});
			}
			else
			{
				break;
			}
		}
	}
	board[amazonX][amazonY] = moveColor;
	return arrs;
}
void Board::applyMove(int index)
{
	std::array<int, 6> moveNums = indexToMove(index);
	board[moveNums[2]][moveNums[3]] = turn;
	int amaIndex = locationToIndex(moveNums[0], moveNums[1]);
	if (turn == S::WHITE)
	{
		int amazon;
		for (int  i = 0; i < 4; i++)
		{
			if (whiteAmazons[i] == amaIndex)
			{
				amazon = i;
				break;
			}
		}
		whiteAmazons[amazon] = locationToIndex(moveNums[2], moveNums[3]);
		turn = S::BLACK;
	}
	else
	{
		int amazon;
		for (int i = 0; i < 4; i++)
		{
			if (blackAmazons[i] == amaIndex)
			{
				amazon = i;
				break;
			}
		}
		blackAmazons[amazon] = locationToIndex(moveNums[2], moveNums[3]);
		turn = S::WHITE;
	}
	board[moveNums[0]][moveNums[1]] = S::EMPTY;
	board[moveNums[4]][moveNums[5]] = S::ARROW;
}
py::tuple Board::neuralworkInput()
{
	std::array<std::array<int, 10>,10> playerPos;
	std::array<std::array<int, 10>, 10 > opponetPos;
	std::array<std::array<int, 10>, 10 > arrowsPos;
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			if (board[i][j] == S::EMPTY)
			{
				playerPos[i][j] = 0;
				opponetPos[i][j] = 0;
				arrowsPos[i][j] = 0;
			}
			else if (board[i][j] == turn)
			{
				playerPos[i][j] = 1;
				opponetPos[i][j] = 0;
				arrowsPos[i][j] = 0;
			}
			else if (board[i][j] == S::ARROW)
			{
				playerPos[i][j] = 0;
				opponetPos[i][j] = 0;
				arrowsPos[i][j] = 1;
			}
			else
			{
				playerPos[i][j] = 0;
				opponetPos[i][j] = 1;
				arrowsPos[i][j] = 0;
			}
		}
	}
	return py::make_tuple(playerPos, opponetPos, arrowsPos);
}


Board::Board()
{
	for (auto& b : board)
	{
		b.fill(S::EMPTY);
	}
	board[0][3] = S::BLACK;
	blackAmazons[0] = 3;
	board[0][6] = S::BLACK;
	blackAmazons[1] = 6;
	board[3][0] = S::BLACK;
	blackAmazons[2] = 30;
	board[3][9] = S::BLACK;
	blackAmazons[3] = 39;
	board[6][0] = S::WHITE;
	whiteAmazons[0] = 60;
	board[6][9] = S::WHITE;
	whiteAmazons[1] = 69;
	board[9][3] = S::WHITE;
	whiteAmazons[2] = 93;
	board[9][6] = S::WHITE;
	whiteAmazons[3] = 96;

	turn = S::WHITE;
}
Board::Board(const Board& aBoard)
{
	board = aBoard.board;
	for (int i = 0; i < 4; i++)
	{
		blackAmazons[i] = aBoard.blackAmazons[i];
		whiteAmazons[i] = aBoard.whiteAmazons[i];
	}
	turn = aBoard.turn;
}

inline int Board::locationToIndex(int x, int y)
{
	return 10 * x + y;
}
inline std::array<int, 2> Board::indextoLocation(int index)
{
	std::array<int, 2> loc;
	loc[0] = index / 10;
	loc[1] = index % 10;
	return loc;
}
inline int Board::moveToIndex(int fromR, int fromC, int toR, int toC, int arrR, int arrC)
{
	return (fromR * 10 + fromC) * 10000 + (toR * 10 + toC) * 100 + arrR * 10 + arrC;
}
inline std::array<int, 6> Board::indexToMove(int index)
{
	std::array<int, 6> move;
	for (int i = 5; i >= 0; i--)
	{
		move[i] = index % 10;
		index /= 10;
	}
	return move;
}
