FROM python:3.9.2

# Add ssh demon
RUN apt-get update && apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    # SSH login fix. Otherwise user is kicked off after login
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
    echo 'cd /app/src' >> /root/.bashrc

COPY ./src/.meta/ /app/src/.meta/
RUN pip install --pre -U -r /app/src/.meta/packages.dev

VOLUME ["/app"]
COPY ./docker/backend/start.sh ./docker/wait-for-it.sh /scripts/
WORKDIR /app/src

ENTRYPOINT ["/scripts/start.sh"]
