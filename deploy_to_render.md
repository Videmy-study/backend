# Deploy Videmy Study Backend to Render

## Prerequisites
- GitHub repository with your code
- Render account (free tier available)
- MongoDB database (MongoDB Atlas recommended)
- Google API key for Gemini

## Step-by-Step Deployment

### 1. Prepare Your Repository
Make sure your code is pushed to GitHub with the following files:
- `requirements.txt`
- `start_server.py` or `Procfile`
- `render.yaml` (optional but recommended)

### 2. Set Up MongoDB (if using)
1. Create a MongoDB Atlas account
2. Create a new cluster
3. Get your connection string
4. Add network access for Render's IPs

### 3. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Review the configuration and click "Apply"

#### Option B: Manual Setup
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `videmy-study-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 start_server.py`
   - **Root Directory:** `backend` (if your code is in a backend folder)

### 4. Set Environment Variables
In the Render dashboard, add these environment variables:

#### Required Variables:
- `MONGODB_URI`: Your MongoDB connection string
- `GOOGLE_API_KEY`: Your Google Gemini API key

#### Optional Variables:
- `HOST`: `0.0.0.0` (default)
- `PORT`: `10000` (Render will set this automatically)
- `NEWS_API_KEY`: For political news agent
- `GUARDIAN_API_KEY`: For Guardian news API
- `NYT_API_KEY`: For New York Times API

### 5. Configure Health Check
- **Health Check Path:** `/chat/health`
- **Health Check Timeout:** `180` seconds

### 6. Deploy
1. Click "Create Web Service"
2. Wait for the build to complete (usually 2-5 minutes)
3. Your API will be available at: `https://your-service-name.onrender.com`

## Testing Your Deployment

### Test Health Check
```bash
curl https://your-service-name.onrender.com/chat/health
```

### Test Chat API
```bash
curl -X POST "https://your-service-name.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how can you help me?",
    "user_id": "test_user"
  }'
```

### Test Available Agents
```bash
curl https://your-service-name.onrender.com/chat/agents
```

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **App Won't Start**
   - Check the logs for error messages
   - Verify environment variables are set correctly
   - Ensure the app binds to `0.0.0.0` and uses `$PORT`

3. **Health Check Fails**
   - Verify the `/chat/health` endpoint works locally
   - Check if the app is starting properly
   - Increase health check timeout if needed

4. **MongoDB Connection Issues**
   - Verify MongoDB URI is correct
   - Check if MongoDB Atlas network access allows Render IPs
   - Ensure MongoDB cluster is running

### Useful Commands:
```bash
# Check if your app works locally
python3 start_server.py

# Test with curl locally
curl http://localhost:8000/chat/health

# Check logs in Render dashboard
# (Go to your service → Logs tab)
```

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MONGODB_URI` | Yes | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `GOOGLE_API_KEY` | Yes | Google Gemini API key | `AIzaSyC...` |
| `HOST` | No | Server host | `0.0.0.0` |
| `PORT` | No | Server port | `10000` |
| `NEWS_API_KEY` | No | News API key | `abc123...` |
| `GUARDIAN_API_KEY` | No | Guardian API key | `abc123...` |
| `NYT_API_KEY` | No | NYT API key | `abc123...` |

## Cost Considerations

- **Free Tier:** 750 hours/month, 512MB RAM, shared CPU
- **Paid Plans:** Start at $7/month for dedicated resources
- **Database:** MongoDB Atlas has a free tier (512MB)

## Next Steps

1. Set up a custom domain (optional)
2. Configure SSL certificates (automatic with Render)
3. Set up monitoring and alerts
4. Configure auto-scaling if needed 