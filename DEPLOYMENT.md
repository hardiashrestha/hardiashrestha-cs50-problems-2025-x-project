# Deployment Guide for Vercel

## Changes Made for Vercel Compatibility

### 1. Fixed Secret Key
- Changed from `os.urandom(24)` to environment variable
- Now uses `SECRET_KEY` from environment with fallback

### 2. Added Database Initialization
- Added `db.create_all()` within app context
- Ensures tables are created on serverless startup

### 3. Added Error Handling
- Registration route now has try-except blocks
- Login route now has try-except blocks  
- All errors are logged to Vercel console
- User-friendly error messages displayed

### 4. Created Vercel Configuration
- `vercel.json` - Vercel deployment configuration
- `.vercelignore` - Files to exclude from deployment
- `.env.example` - Environment variables template

## Deployment Steps

### Step 1: Set Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:

```
SECRET_KEY=your-random-secret-key-here
API_SPORTS_KEY=your-api-sports-key
API_SPORTS_HOST=api-football-v1.p.rapidapi.com
```

To generate a secure SECRET_KEY:
```python
import secrets
print(secrets.token_hex(32))
```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel CLI
```bash
npm i -g vercel
vercel login
vercel
```

#### Option B: Deploy via GitHub
1. Push code to GitHub
2. Connect repository to Vercel
3. Vercel will auto-deploy on push

## Important Notes

### SQLite Database Limitations

⚠️ **CRITICAL**: SQLite on Vercel is **EPHEMERAL**
- Data is stored in `/tmp` directory
- Data is LOST on every deployment
- Data is LOST when serverless functions scale down

### Recommended Production Database Solutions

For production, use a cloud database:

1. **Vercel Postgres** (Recommended)
   - Native Vercel integration
   - Easy setup

2. **Supabase PostgreSQL**
   - Free tier available
   - Good for learning

3. **PlanetScale MySQL**
   - Generous free tier
   - Serverless MySQL

4. **MongoDB Atlas**
   - Free tier available
   - NoSQL option

### To Migrate to PostgreSQL:

1. Update requirements.txt:
```
psycopg2-binary==2.9.9
```

2. Update database URI in app.py:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///f1users.db'  # Fallback for local dev
)
```

3. Add DATABASE_URL to Vercel environment variables

## Testing Locally

1. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your actual values
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python app.py
```

## Troubleshooting

### Registration Error
- Check Vercel logs for detailed error messages
- Verify SECRET_KEY is set in environment variables
- Ensure database connection is working

### Internal Server Error
- Check Vercel Function Logs
- Look for Python stack traces
- Verify all dependencies in requirements.txt

## Next Steps

1. ✅ Code is ready for deployment
2. ⚠️ Consider migrating to PostgreSQL for production
3. 📝 Set up environment variables in Vercel
4. 🚀 Deploy and test!

