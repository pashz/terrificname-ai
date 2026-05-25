#!/bin/bash
# keep-alive.sh — 1-line ping to prevent Render free tier from sleeping
# Run this on UptimeRobot (free) or any cron service:
#   curl -s https://your-app.onrender.com/health > /dev/null
# Or run locally via cron every 10 minutes:
#   */10 * * * * curl -s https://your-app.onrender.com/health > /dev/null 2>&1

curl -s -o /dev/null -w "%{http_code}" https://$1/health
