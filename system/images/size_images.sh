#!/bin/bash

find . -type f -name "*.jpg" -exec du -ch {} + | grep total$