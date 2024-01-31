#!/bin/bash

CPP_FILE="capture.cpp"

EXE_FILE="bin/capture"

g++ -o $EXE_FILE $CPP_FILE $(pkg-config --cflags --libs libzmq)

# Check if the compilation was successful
if [ $? -eq 0 ]; then
  echo "Compilation successful."
else
  echo "Compilation failed."
fi
