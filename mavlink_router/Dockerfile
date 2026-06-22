FROM debian:bookworm AS builder
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git meson ninja-build pkg-config gcc g++ systemd
RUN git clone --recursive https://github.com/mavlink-router/mavlink-router
WORKDIR /mavlink-router
RUN meson setup build . --buildtype=release
RUN ninja -C build install

FROM debian:bookworm-slim
COPY --from=builder /usr/bin/mavlink-routerd /usr/bin/mavlink-routerd 
COPY main.conf .
CMD ["/usr/bin/mavlink-routerd","-c","main.conf"]
