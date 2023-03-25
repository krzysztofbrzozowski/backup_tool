FROM alpine

RUN apk add openrc openssh \
    && mkdir -p /run/openrc \
    && touch /run/openrc/softlevel

ENTRYPOINT ["sh", "-c", "rc-status; rc-service sshd start"]