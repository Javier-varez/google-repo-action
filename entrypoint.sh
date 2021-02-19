#!/bin/sh -xe

git config --global user.name "dummy"
git config --global user.email "dummy@example.com"
git config --global color.diff "white"

repo init -u $1 -q
repo sync -c -d -j$(nproc) -q

