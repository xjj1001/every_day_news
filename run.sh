#!/bin/bash
echo "666666"
cat add.csv
echo "1,2,3" >> add.csv
git status
git add add.csv
git commit -m 'update add.csv'
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git push origin main

