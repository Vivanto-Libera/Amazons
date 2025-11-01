#ifndef BOARD_H
#define BOARD_H
#include <pybind11/pybind11.h>
#include <map>
#include <vector>

namespace py = pybind11;
using namespace pybind11::literals;

class Board
{
public:
	static const std::map<py::tuple, int> moveToIndexMap;
	static const std::map<int, py::tuple> indexToMoveMap;
	static const int rowDirection[8];
	static const int colDirection[8];

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

	py::tuple isTerminal();
	std::vector<int> legalMoves();

	static int moveToIndex(py::tuple move);
	static py::tuple indexToMove(int index);

	Board();
	Board(const Board& aBoard);
private:
	std::vector<py::tuple> arrows(py::tuple amazon, int row, int col);
};
#endif
