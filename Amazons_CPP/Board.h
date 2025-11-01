#ifndef BOARD_H
#define BOARD_H
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <map>
#include <vector>
#include <string>
#include <array>

namespace py = pybind11;
using namespace pybind11::literals;

class Board
{
public:
	static const int rowDirection[8];
	static const int colDirection[8];

	enum State
	{
		EMPTY=0,
		WHITE=-1,
		BLACK=1,
		ARROW=2,
	};
	State board[10][10];
	int blackAmazons[4];
	int whiteAmazons[4];
	State turn;

	State isTerminal();
	std::vector<int> legalMoves();
	void applyMove(int index);
	py::tuple neuralworkInput();

	static int moveToIndex(int fromR, int fromC, int toR, int toC, int arrR, int arrC);
	static std::array<int, 6> indexToMove(int index);
	static int locationToIndex(int x, int y);
	static std::array<int, 2> indextoLocation(int index);

	Board();
	Board(const Board& aBoard);
private:
	std::vector<std::array<int ,2>> arrows(int amazonX, int amazonY, int row, int col);
};
#endif
