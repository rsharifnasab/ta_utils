#!/bin/bash 

astyle */*/*.c*
find . -name '*.orig' -delete
