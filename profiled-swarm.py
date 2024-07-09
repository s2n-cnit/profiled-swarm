#!/usr/bin/env -S --chdir=/axc-mgmt/github/tnt-s2n-cnit/profiled-swarm poetry run python

from clize import run
from generator import generator

if __name__ == "__main__":
    run(generator)
