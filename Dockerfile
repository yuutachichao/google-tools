FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
ca-certificates \
curl \
bash \
git \
build-essential \
pkg-config \
libssl-dev \
python3 \
python3-pip \
python3-venv \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN echo "DOCKERFILE_V3_MARKER"

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN git clone https://github.com/googleworkspace/cli.git /tmp/googleworkspace-cli \
&& cd /tmp/googleworkspace-cli \
&& cargo build --release \
&& cp target/release/gws /usr/local/bin/gws \
&& chmod +x /usr/local/bin/gws \
&& rm -rf /tmp/googleworkspace-cli

RUN mkdir -p /root/.config/gws /data/gws

COPY requirements.txt /app/requirements.txt

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main.py /app/main.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
