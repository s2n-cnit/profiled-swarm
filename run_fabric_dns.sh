#!/bin/bash

fab -R dns hping3_gen_dns_$1 &
