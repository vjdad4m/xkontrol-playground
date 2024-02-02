#!/bin/bash

# Compile zmq client

CPP_FILE="capture.cpp"

EXE_FILE="bin/capture"

g++ -o $EXE_FILE $CPP_FILE $(pkg-config --cflags --libs libzmq)

# Check if the compilation was successful
if [ $? -eq 0 ]; then
  echo "Compilation successful."
else
  echo "Compilation failed."
fi

# Compile jstick controller driver

CPP_FILE="jstick.cpp"

EXE_FILE="bin/jstick"

g++ -o $EXE_FILE $CPP_FILE

# Check if the compilation was successful
if [ $? -eq 0 ]; then
  echo "Compilation successful."
else
  echo "Compilation failed."
fi
