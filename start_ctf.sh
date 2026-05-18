#!/bin/bash
echo "=== DEMARRAGE CTF FORTERESSE ==="

# Verifier que les dockers tournent
echo "Verification dockers..."
docker-compose -f ~/ignavia-tech/docker-compose.yml up -d

# Vider les alertes
echo "Reset alertes..."
curl -s http://localhost:8080/events/clear

# Lancer surveillance Cowrie
echo "Demarrage surveillance Cowrie..."
pkill -f cowrie_watch.sh 2>/dev/null
nohup ~/ignavia-tech/cowrie_watch.sh > ~/ignavia-tech/cowrie_watch.log 2>&1 &

echo "=== CTF PRET ==="
