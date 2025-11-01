#include "Board.h"

using S = Board::State;

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
	board[0][6] = S::BLACK;
	board[3][0] = S::BLACK;
	board[3][9] = S::BLACK;
	board[6][0] = S::WHITE;
	board[6][9] = S::WHITE;
	board[9][3] = S::WHITE;
	board[9][6] = S::WHITE;
}