#!/bin/bash

file_extensions=".py"

# Find all files with specified extensions in the current directory and subdirectories
files=$(find . -type f -name "*$file_extensions")

# Format each file using black
for file in $files; do
  black "$file"
done
