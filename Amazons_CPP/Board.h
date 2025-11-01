#ifndef BOARD_H
#define BOARD_H
#include <pybind11/pybind11.h>
#include <map>

namespace py = pybind11;
using namespace pybind11::literals;

class Board
{
public:
	static const std::map<py::tuple, int> moveToIndexMap;
	static const std::map<int, py::tuple> indexToMoveMap;
	enum State
	{
		EMPTY,
		WHITE,
		BLACK,
		ARROW,
	};
	State board[10][10];
	py::tuple blackAmazons[4];
	py::tuple whiteAmazons[4];
	State turn;

	static int moveToIndex(py::tuple move);
	static py::tuple indexToMove(int index);

	Board();
	Board(const Board& aBoard);
};
#endif
