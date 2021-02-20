#!/bin/sh -xe

MANIFEST_URL="https://github.com/${1}"
MANIFEST_BRANCH="${2}"
MANIFEST_FILE="${3}"
MANIFEST_GROUP="${4}"
CHECKOUT_DEPENDENCIES=${5}
ORIGIN_REPO=${6}
GENERATED_MANIFEST=${7}

git config --global user.name "dummy"
git config --global user.email "dummy@example.com"
git config --global color.diff "white"

REPO_INIT_ARGS="-u ${MANIFEST_URL} -q -b ${MANIFEST_BRANCH} -m ${MANIFEST_FILE} -g ${MANIFEST_GROUP}"

repo init ${REPO_INIT_ARGS}
repo sync -c -d -j$(nproc) -q

if [ "${CHECKOUT_DEPENDENCIES}" = "true" ]
then
  /tools/checkout_deps.py ${GITHUB_REF} ${ORIGIN_REPO}
fi

if [ ! -z "${GENERATED_MANIFEST}" ]
then
  repo manifest -r -o ${GENERATED_MANIFEST}
fi

chmod -R a+rw .

