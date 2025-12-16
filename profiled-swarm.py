#!/usr/bin/env -S uv --directory /axc-mgmt/github/s2n-cnit/profiled-swarm run python

from clize import run
from generator import generator

if __name__ == "__main__":
    run(generator)
