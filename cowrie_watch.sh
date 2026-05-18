#!/bin/bash
SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)

docker logs cowrie -f --since "$SINCE" 2>&1 | while read line; do
    if echo "$line" | grep -q "login attempt.*succeeded"; then
        IP=$(echo "$line" | grep -oP '\d+\.\d+\.\d+\.\d+')
        USER=$(echo "$line" | grep -oP "b'\K[^']+" | head -1)
        if echo "$IP" | grep -qP '^10\.'; then
            curl -s -X POST http://localhost:8080/alerte/cowrie \
                 -d "Connexion honeypot SSH - IP: $IP - User: $USER"
        fi
    fi
done
