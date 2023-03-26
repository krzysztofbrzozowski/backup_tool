FROM alpine

RUN apk add --no-cache \
        openssh \
    && ssh-keygen -A \
    && mkdir /root/.ssh \
    # This is secret generated only for docker purposes
    && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFWQPMqG1nVqs1xyAIOxOTIGI8q8X6uLfX3G82Gm1ufc root" > /root/.ssh/authorized_keys \
    && chmod 0700 /root/.ssh \
    && echo "root:root" | chpasswd \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

EXPOSE 22

ENTRYPOINT ["/usr/sbin/sshd", "-D", "-e"]
#ENTRYPOINT ["/usr/sbin/sshd"]