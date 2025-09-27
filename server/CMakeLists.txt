cmake_minimum_required(VERSION 3.10)
project(kahoot_server)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Boost system library
find_package(Boost REQUIRED COMPONENTS system)
find_package(Threads REQUIRED)

# Include our headers (json.hpp)
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add executable
add_executable(kahoot_server kahoot_server.cpp)

# Link libraries
target_link_libraries(kahoot_server
    Boost::system
    Threads::Threads
)
