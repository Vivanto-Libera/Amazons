# CMakeList.txt : CMake project for Amazons_CPP, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("Amazons_CPP")
set(PYBIND11_FINDPYTHON ON)
add_subdirectory(extern/pybind11)
pybind11_add_module(Amazons Board.h Board.cpp)
install (TARGETS Amazons DESTINATION .)


set(Torch_DIR ${CMAKE_SOURCE_DIR}/extern/libtorch/share/cmake/Torch)
find_package(Torch REQUIRED)

# Add source to this project's executable.
target_link_libraries(Amazons PRIVATE "${TORCH_LIBRARIES}")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET Amazons PROPERTY CXX_STANDARD 20)
endif()

# TODO: Add tests and install targets if needed.
