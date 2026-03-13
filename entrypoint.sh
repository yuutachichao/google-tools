#!/usr/bin/env bash
set -e

mkdir -p /root/.config/gws /data/gws

for f in .encryption_key client_secret.json credentials.enc token_cache.json; do
if [ -f "/data/gws/$f" ]; then
cp "/data/gws/$f" "/root/.config/gws/$f"
fi
done

chmod 600 /root/.config/gws/.encryption_key 2>/dev/null || true
chmod 600 /root/.config/gws/client_secret.json 2>/dev/null || true
chmod 600 /root/.config/gws/credentials.enc 2>/dev/null || true
chmod 600 /root/.config/gws/token_cache.json 2>/dev/null || true

exec "$@"
