# better-enums - header-only reflective enums for C++17 and newer.
#
# This file exposes the library as a CMake interface target so it can be
# consumed as a dependency, e.g. through CPM.cmake:
#
#   cpmaddpackage(
#     NAME
#     better-enums
#     GIT_REPOSITORY
#     https://github.com/<your-org>/better-enums
#     GIT_TAG
#     <your-tag-or-branch>
#   )
#   target_link_libraries(<your-target> PRIVATE better_enums::better_enums)
#
# CPM runs this CMakeLists.txt (add_subdirectory) and the consumer links the
# better_enums::better_enums target, which carries the repository root as an
# include directory so `#include <enum.h>` works.

cmake_minimum_required(VERSION 3.14)

project(better_enums
    VERSION 0.12.1
    DESCRIPTION "Header-only reflective enums for C++17+"
    LANGUAGES CXX)

# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------

# Build (and, when enabled, run) the better-enums test suite. Off by default so
# that consumers of the package are not forced to pull in the cxxtest-based
# test dependencies.
option(BUILD_BETTER_ENUM_TESTS "Build and run the better-enums test suite" OFF)

# ---------------------------------------------------------------------------
# Library target
# ---------------------------------------------------------------------------

# Header-only library: an INTERFACE target. The repository root is where
# enum.h lives, so exposing it as an include directory makes
# `#include <enum.h>` work for every consumer of this target.
add_library(better_enums INTERFACE)
add_library(better_enums::better_enums ALIAS better_enums)

target_include_directories(better_enums INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

# Header-only, but the (optional) std::optional integration requires C++17.
target_compile_features(better_enums INTERFACE cxx_std_17)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if(BUILD_BETTER_ENUM_TESTS)
    # The test suite lives in test/ and is orchestrated by its own Makefile,
    # which builds and runs the full configuration matrix (C++98/11/14/17 and
    # the constexpr/strict-conversion variants).
    #
    # The Makefile's all-configurations target requires MAKE_COMMAND and
    # OUTPUT_DIRECTORY to be set (the unix/ms wrappers normally provide them),
    # so pass them here.
    set(BETTER_ENUMS_TEST_COMMAND
        make MAKE_COMMAND=make OUTPUT_DIRECTORY=. all-configurations)

    # The tests are enforced through a dedicated build target rather than being
    # silently attached to the default `all` build: CMake 4.x no longer exposes
    # `all` as a dependable logical target, and the BUILD_BYDEFAULT property does
    # not pull custom targets into `all`, so there is no reliable way to run the
    # suite as part of a plain `cmake --build .` from a consuming project. The
    # dedicated target makes running the suite explicit and unavoidable whenever
    # the option is enabled:
    #
    #   cmake --build . --target better_enums_tests
    #
    add_custom_target(better_enums_tests
        COMMAND ${BETTER_ENUMS_TEST_COMMAND}
        COMMENT "Running the better-enums test suite"
        VERBATIM
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/test")

    # ctest integration for CI workflows. Works when the consuming project also
    # enables testing (e.g. it calls enable_testing() / include(CTest)); run with
    # `ctest` from the top-level build directory.
    include(CTest)
    add_test(NAME better_enums_tests
        COMMAND ${BETTER_ENUMS_TEST_COMMAND}
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/test")
endif()

# ---------------------------------------------------------------------------
# Installation (install the header and the exported target)
# ---------------------------------------------------------------------------

include(GNUInstallDirs)

install(TARGETS better_enums EXPORT better_enums-targets)

# Install the header next to the exported target's include directory. The
# better_enums target carries that directory as an INTERFACE include property,
# so a package that exports this target can ship `#include <enum.h>` after
# install.
install(FILES enum.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT better_enums-targets
    NAMESPACE better_enums::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/better_enums)
