#!/bin/sh
if [ $# -eq 0 ]; then
  echo "get arg error"
  exit 1
fi

mkdir tmp
echo "-----BEGIN OPENSSH PRIVATE KEY-----" > tmp/id_ed25519_docker
echo "$1" >> tmp/id_ed25519_docker
echo "-----END OPENSSH PRIVATE KEY-----" >> tmp/id_ed25519_docker

realpath tmp/id_ed25519_docker
cat tmp/id_ed25519_docker
