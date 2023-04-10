#!/bin/sh
if [ $# -eq 0 ]; then
  echo "get arg error"
  exit 1
fi

echo "-----BEGIN OPENSSH PRIVATE KEY-----" > id_ed25519_docker
echo "$1" >> id_ed25519_docker
echo "-----END OPENSSH PRIVATE KEY-----" >> id_ed25519_docker

realpath id_ed25519_docker
cat id_ed25519_docker
