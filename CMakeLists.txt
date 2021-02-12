cmake_minimum_required(VERSION 2.8.6)
project(brotli)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64" CACHE STRING "OSX Architectures" FORCE)

FILE(GLOB_RECURSE enc enc/*.cc)
FILE(GLOB_RECURSE dec dec/*.c)
list(FILTER dec EXCLUDE REGEX ".*dec[/]dictionary[.]c$") # this is a duplicate of definitions in enc

add_executable(brotli ${enc} ${dec} tools/bro.cc)
