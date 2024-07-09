#!/usr/bin/env -S poetry -C /axc-mgmt/github/tnt-s2n-cnit/profiled-swarm run python

from clize import run
from generator import generator

if __name__ == "__main__":
    run(generator)
