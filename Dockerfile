FROM ubuntu:latest

WORKDIR /home

# Setup tools to work in the container
RUN apt-get update && apt-get install -y \
    curl \ 
    libdigest-sha-perl \
    && curl -sLSf https://inletsctl.inlets.dev | sh \
    && inletsctl download \
    && export UPSTREAM=http://192.168.0.11:80

CMD inlets client --remote "ws://165.22.127.169:8080" \
    --token "DBhB9Mw2MGExiLF96F2EcQyOvG7nHlQVdJ5bjIBg776EbadgyUuzVSwmpxaMfuwI" \
    --upstream $UPSTREAM