#!/usr/bin/env -S poetry -C /axc-mgmt/github/s2n-cnit/profiled-swarm run python

from clize import run
from generator import generator
from manager import manager

if __name__ == "__main__":
    run(generator, alt=manager)
