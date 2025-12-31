#!/bin/bash
# Get cloudflared tunnel URL
curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tunnels' in data and len(data['tunnels']) > 0:
        print('🌐 Public URL:', data['tunnels'][0]['public_url'])
    else:
        print('No tunnel found')
except:
    print('No active tunnel')
"

