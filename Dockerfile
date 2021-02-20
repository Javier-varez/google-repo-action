# Container image that runs your code
FROM ubuntu:20.04

RUN apt update && \
    apt install -y git openssh-client curl python3 python

# Install google repo
RUN curl https://storage.googleapis.com/git-repo-downloads/repo > /usr/bin/repo && \
    chmod +x /usr/bin/repo

COPY checkout_deps.py /tools/checkout_deps.py
COPY manifest_parser.py /tools/manifest_parser.py

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
