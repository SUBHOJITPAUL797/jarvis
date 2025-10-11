# Jarvis Assistant - Render Deployment Guide

## 🚀 Quick Deploy to Render

This is a simplified version of Jarvis Assistant optimized for Render deployment. It includes only the web-based chat interface with AI capabilities.

## Features (Web Version)
- ✅ Web-based chat interface
- ✅ AI chatbot powered by Google Gemini
- ✅ Clean, modern UI
- ✅ No local dependencies required

## Removed Features (for web deployment)
- ❌ Face authentication (requires camera)
- ❌ Voice commands (requires microphone)
- ❌ Hotword detection (requires local audio)
- ❌ System app opening (requires OS access)
- ❌ WhatsApp integration (requires desktop)
- ❌ YouTube control (requires desktop)

## Deploy to Render

### Step 1: Fork/Clone Repository
1. Fork or clone this repository to your GitHub account

### Step 2: Create Render Account
1. Sign up at [render.com](https://render.com)
2. Connect your GitHub account

### Step 3: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure the service:
   - **Name**: `jarvis-assistant` (or your choice)
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements_render.txt`
   - **Start Command**: `python app_render.py`
   - **Instance Type**: Free

### Step 4: Set Environment Variables
In the Render dashboard, add:
- `GEMINI_API_KEY`: Your Google Gemini API key
  - Get it from: [Google AI Studio](https://makersuite.google.com/app/apikey)

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment (usually 2-5 minutes)
3. Access your app at: `https://your-app-name.onrender.com`

## File Structure for Render

```
├── app_render.py              # Main application file for Render
├── requirements_render.txt    # Minimal dependencies
├── render.yaml               # Render configuration
├── backend/
│   ├── command_render.py    # Simplified command handling
│   └── feature_render.py    # Web-only features
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css           # Styles
│   ├── controller.js       # Frontend logic
│   └── assets/             # Static assets
└── .env.example            # Environment variables template
```

## Local Testing

To test locally before deployment:

```bash
# Install dependencies
pip install -r requirements_render.txt

# Set environment variable
export GEMINI_API_KEY="your-api-key-here"

# Run the app
python app_render.py

# Access at http://localhost:10000
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `PORT` | Server port (auto-set by Render) | Auto |

## Troubleshooting

### App not loading?
- Check if build succeeded in Render dashboard
- Verify environment variables are set
- Check logs in Render dashboard

### AI not responding?
- Verify `GEMINI_API_KEY` is set correctly
- Check API key quotas at Google AI Studio
- Review error logs in Render dashboard

### Port issues?
- Render automatically sets the PORT variable
- Don't hardcode ports in the application

## Cost

- **Render Free Tier**: 
  - 750 hours/month
  - Spins down after 15 minutes of inactivity
  - May have cold start delays

- **Google Gemini API**:
  - Free tier available
  - Check current limits at Google AI Studio

## Support

For issues specific to:
- **Render deployment**: Check [Render docs](https://render.com/docs)
- **Google Gemini API**: Visit [Google AI docs](https://ai.google.dev/docs)

## Important Notes

1. This is a simplified version for web deployment only
2. No audio/video features are available
3. All interactions are text-based
4. The app will spin down on Render's free tier after inactivity

## Next Steps

After successful deployment:
1. Share your app URL with users
2. Monitor usage in Render dashboard
3. Upgrade to paid tier if needed for always-on availability

---

**Ready to deploy!** Follow the steps above to get your Jarvis Assistant running on Render in minutes! 🎉