#!/bin/sh -xe

MANIFEST_URL="https://github.com/${1}"
CHECKOUT_DEPENDENCIES=${2}
ORIGIN_REPO=${3}

git config --global user.name "dummy"
git config --global user.email "dummy@example.com"
git config --global color.diff "white"

repo init -u $MANIFEST_URL -q
repo sync -c -d -j$(nproc) -q

if [ "${CHECKOUT_DEPENDENCIES}" = "true" ]
then
  /tools/checkout_deps.py ${GITHUB_REF} ${ORIGIN_REPO}
fi

chmod -R a+rw .

