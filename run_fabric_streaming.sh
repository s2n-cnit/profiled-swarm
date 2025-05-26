#!/bin/bash

fab -R streaming_a hping3_gen_streaming_a_$1 &
fab -R streaming_b hping3_gen_streaming_b_$1 &
fab -R streaming_c hping3_gen_streaming_c_$1 &
fab -R streaming_d hping3_gen_streaming_d_$1 &
