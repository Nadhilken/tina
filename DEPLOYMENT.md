# Deployment Guide for Render

## Prerequisites

1. **GitHub Repository**: Push your code to a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Required Images**: Ensure you have added the required images:
   - `static/images/i_robotics_logo.png`
   - `static/images/your-gif.gif`

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository contains all the required files:
- ✅ `app.py` - Main Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Process file
- ✅ `runtime.txt` - Python version
- ✅ `templates/index.html` - HTML template
- ✅ `qa_data.json` - Q&A data
- ✅ `static/` directory with required images

### 2. Connect to Render

1. Go to [render.com](https://render.com) and sign up/log in
2. Click "New +" and select "Web Service"
3. Connect your GitHub account
4. Select your repository (`receptoweb`)

### 3. Configure the Web Service

Use these settings:

**Basic Settings:**
- **Name**: `voice-qa-app` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Advanced Settings:**
- **Python Version**: `3.11.5`
- **Auto-Deploy**: `Yes` (recommended)

### 4. Environment Variables (Optional)

You can add these environment variables if needed:
- `PYTHON_VERSION`: `3.11.5`
- `PORT`: `10000` (Render will set this automatically)

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application

### 6. Verify Deployment

1. Wait for deployment to complete (usually 2-5 minutes)
2. Click on your service URL to test
3. Test voice recognition functionality
4. Verify all features work correctly

## Troubleshooting

### Common Issues:

**1. Build Fails**
- Check `requirements.txt` for correct dependencies
- Ensure Python version compatibility

**2. App Won't Start**
- Verify `app.py` has correct port configuration
- Check application logs in Render dashboard

**3. Static Files Not Loading**
- Ensure `static/` directory structure is correct
- Check file paths in templates

**4. Images Not Displaying**
- Verify image files exist in `static/images/`
- Check file names match HTML references exactly

### Logs and Debugging:

1. Go to your Render dashboard
2. Click on your service
3. Check "Logs" tab for error messages
4. Monitor "Events" tab for deployment status

## Post-Deployment

### Custom Domain (Optional):
1. Go to Settings → Custom Domains
2. Add your domain
3. Configure DNS records as instructed

### Monitoring:
- Check application health regularly
- Monitor usage and performance
- Set up alerts for downtime

## Free Tier Limitations

Render's free tier includes:
- 750 hours/month (enough for one always-on service)
- Services sleep after 15 minutes of inactivity
- 15-30 second cold start time

For production use, consider upgrading to a paid plan.

## Security Notes

- Uploaded files are stored temporarily
- Consider implementing user authentication
- Regularly backup your Q&A data
- Monitor for abuse if publicly accessible

## Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Verify all files are properly committed to Git
4. Ensure images are uploaded to the correct directories