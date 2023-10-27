#!/bin/bash
echo "666666"
echo "1,2,3" >> add.csv
git status
git add add.csv
git commit -m 'update add.csv'
git push origin main
