#!/bin/sh
if [ $# -eq 0 ]; then
  echo "get arg error"
  exit 1
fi

echo "-----BEGIN OPENSSH PRIVATE KEY-----" > tests/id_ed25519_docker
echo "$1" >> tests/id_ed25519_docker
echo "-----END OPENSSH PRIVATE KEY-----" >> tests/id_ed25519_docker

realpath tests/id_ed25519_docker
cat tests/id_ed25519_docker
