#include "Board.h"

PYBIND11_MODULE(Amazons, m)
{
	py::enum_<Board::State>(m, "State")
		.value("EMPTY", Board::State::EMPTY)
		.value("WHITE", Board::State::WHITE)
		.value("BLACK", Board::State::BLACK)
		.value("ARROW", Board::State::ARROW)
		.export_values();
	py::class_<Board>(m, "Board")
		.def(py::init<>())
		.def(py::init<const Board&>())
		.def("isTerminal", &Board::isTerminal)
		.def("legalMoves", &Board::legalMoves)
		.def("neuralworkInput", &Board::neuralworkInput)
		.def("applyMove", &Board::applyMove)
		.def_readwrite("board", &Board::board)
		.def_static("indexToMove", &Board::indexToMove)
		.def_static("moveToIndex", &Board::moveToIndex)
		.def_readwrite("turn", &Board::turn);
};