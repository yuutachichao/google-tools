#!/usr/bin/env bash
set -e

mkdir -p /root/.config/gws /data/gws

for f in .encryption_key client_secret.json credentials.enc token_cache.json; do
  if [ -f "/data/gws/$f" ]; then
    cp "/data/gws/$f" "/root/.config/gws/$f"
    chmod 600 "/root/.config/gws/$f"
  fi
done

exec "$@"
