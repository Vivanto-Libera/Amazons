#ifndef BOARD_H
#define BOARD_H
#include <pybind11/pybind11.h>

namespace py = pybind11;

class Board
{
public:
	enum State
	{
		EMPTY,
		WHITE,
		BLACK,
		ARROW,
	};
	State board[10][10];

	Board();
};


#endif
