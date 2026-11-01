#!/usr/bin/env python3
"""Ensure the cxxtest test framework is available.

The better-enums test suite is built with cxxtest
(https://github.com/cxxtest/cxxtest): its ``cxxtestgen`` generator turns the
``test/cxxtest/*.h`` files into a self-contained test runner, and the headers
are compiled into it.

If cxxtest is already installed on the system (``cxxtestgen`` on the PATH), this
script does nothing. Otherwise it creates a local working copy under
``.cxxtest/`` (a shallow git clone) so the tests can still be built offline from
the repository's own point of view.

Usage::

    python3 ensure_cxxtest.py            # resolve cxxtest, print result
    python3 ensure_cxxtest.py --local    # always create a local copy

It prints the cxxtest *root* directory on stdout -- the directory that contains
both the ``cxxtest/`` header subtree and the ``bin/cxxtestgen`` generator.
Nothing is printed (exit status 0) when the system cxxtest is used, in which
case the caller should rely on the compiler's default include path.

The script is idempotent: once a local copy exists it is reused, and a system
installation is always preferred.
"""

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL_DIR = os.path.join(HERE, ".cxxtest")
REPO_URL = "https://github.com/cxxtest/cxxtest.git"


def on_system():
    """Return True if a usable system cxxtest installation is available.

    We require the ``cxxtestgen`` generator to be on the PATH; a normal system
    install places the matching headers on the compiler's default include path
    (``/usr/include/cxxtest``), which CMake then picks up without help.
    """
    return shutil.which("cxxtestgen") is not None


def fetch_local():
    """Create and return a local working copy of cxxtest under ``.cxxtest``."""
    if os.path.isdir(os.path.join(LOCAL_DIR, ".git")):
        return LOCAL_DIR

    print("better-enums tests: cxxtest not found, cloning a local copy ...",
          file=sys.stderr)
    if os.path.isdir(LOCAL_DIR):
        shutil.rmtree(LOCAL_DIR)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, LOCAL_DIR],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        sys.exit(
            "error: failed to clone cxxtest from {0} ({1}). "
            "Install cxxtest on the system, or check your network "
            "connection.".format(REPO_URL, error)
        )
    except FileNotFoundError:
        sys.exit(
            "error: git was not found on the PATH; cannot fetch cxxtest. "
            "Install cxxtest on the system instead."
        )

    return LOCAL_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Ensure the cxxtest test framework is available."
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="always create a local working copy, even if one is on the system",
    )
    args = parser.parse_args()

    if not args.local and on_system():
        # System cxxtest: nothing to do, headers are on the default include path.
        return 0

    root = fetch_local()
    print(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
