#include "Board.h"

PYBIND11_MODULE(Amazons, m, py::mod_gil_not_used())
{
	py::class_<Board>(m, "Board")
		.def(py::init<>())
		.def(py::init<const Board&>())
		.def("isTerminal", &Board::isTerminal)
		.def("legalMoves", &Board::legalMoves)
		.def_static("moveToIndex", &Board::moveToIndex)
		.def_static("indexToMove", &Board::indexToMove)
		.def_readwrite("board",&Board::board)
		.def_readwrite("blackAmazons", &Board::blackAmazons)
		.def_readwrite("whiteAmazons", &Board::whiteAmazons)
		.def_readwrite("turn", &Board::turn);
	py::enum_<Board::State>(m, "State")
		.value("EMPTY", Board::State::EMPTY)
		.value("WHITE", Board::State::WHITE)
		.value("BLACK", Board::State::BLACK)
		.value("ARROW", Board::State::ARROW);
};