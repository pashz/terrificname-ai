# Keep-Alive Setup (Render Free Tier)

Render free tier sleeps after 15 minutes of inactivity. For hackathon judging, you need the app awake.

## Option A: UptimeRobot (Recommended — Free, Zero Maintenance)

1. Go to https://uptimerobot.com and sign up (free)
2. Click "Add New Monitor"
3. Settings:
   - Monitor Type: HTTP(s)
   - Friendly Name: TerrificName AI
   - URL: `https://your-app.onrender.com/health`
   - Monitoring Interval: 5 minutes (free tier allows this)
4. Save. Done.

UptimeRobot will ping your `/health` endpoint every 5 minutes. Your app never sleeps.
Cost: $0. Time: 2 minutes.

## Option B: Cron-Job.org (Alternative Free Service)

1. Go to https://cron-job.org
2. Create job: `curl https://your-app.onrender.com/health`
3. Set interval: every 5 minutes
4. Done.

## Option C: Local Cron (If you have a server/VM running)

```bash
# Edit crontab
crontab -e

# Add this line (pings every 10 minutes)
*/10 * * * * curl -s -o /dev/null https://your-app.onrender.com/health
```

## Confidence Assessment

✅ **High confidence this works.** UptimeRobot has been keeping Render free apps awake for years. It's a standard pattern.
- `/health` endpoint returns instantly (no AI call, just static JSON)
- Zero cost, zero code changes, 2-minute setup
- If UptimeRobot goes down, Cron-Job.org is an identical backup

⚠️ **One caveat**: Render free tier has a monthly hour limit (~750 hrs). UptimeRobot keeps it awake 24/7, which uses ~720 hrs/month. That's fine for a 1-week hackathon sprint. For long-term, upgrade to Render's $7/month plan or switch to Railway.
