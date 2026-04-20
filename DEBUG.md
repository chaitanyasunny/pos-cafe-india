# Debug Guide - Cafe POS

## Common Issues & Solutions

### White/Blank Screen in Browser

**Symptom**: Browser shows blank white page, but server is running.

**Diagnosis**:
```bash
# Check server is actually serving HTML
curl http://127.0.0.1:5555/ | wc -c
# Should return > 10000 bytes

# Check API endpoints work
curl http://127.0.0.1:5555/api/products
curl http://127.0.0.1:5555/api/stats
```

**Fixes** (try in order):
1. Hard refresh: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R` (Windows)
2. Open in private/incognito window
3. Try different browser (Safari → Chrome or vice versa)
4. Use `http://127.0.0.1:5555` instead of `http://localhost:5555`
5. Check browser console (`Cmd+Option+J` on Mac) for JavaScript errors
6. Disable browser extensions (ad blockers can interfere)

### "Access to localhost was denied" in Chrome

Chrome has strengthened localhost security. **Fix**: Use your machine's IP address instead:

```bash
# Get your IP
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
# Returns something like 192.0.0.2

# Then access via
http://YOUR_IP:5555
```

### Port Already in Use

```bash
# Find what's using the port
lsof -i :5555

# Kill the process
lsof -i :5555 | awk 'NR>1 {print $2}' | xargs kill -9
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start if not running
brew services start postgresql@16

# Verify database exists
psql -d cafe_pos -c '\dt'
```

### Database Missing Tables

```bash
# Manually initialize database
/usr/bin/python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Tables created')
"
```

### API Returns 500 Error

Check Flask output in terminal — full traceback will be shown.

### Menu Items Not Loading

Products are seeded on first run. If database was reset:
```bash
# Verify products exist
psql -d cafe_pos -c 'SELECT COUNT(*) FROM products'
# Should return 27

# If 0, restart the app — it will re-seed
```

## Verbose Debugging

To enable Flask debug mode for detailed error pages:

```bash
# Edit app.py
debug=True

# WARNING: Don't use debug=True in production
```

## Check All Processes

```bash
# All processes related to app
ps aux | grep python3 | grep app

# All listening ports
lsof -i -P | grep LISTEN
```
