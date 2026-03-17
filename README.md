# HemmTrack Pro — Backend API

## Railway वर Deploy कसा करायचा?

1. railway.app वर जा → Sign up with GitHub
2. "New Project" → "Deploy from GitHub"
3. हा folder GitHub वर upload करा
4. Railway मध्ये Environment Variables सेट करा:
   - GMAIL_USER = sanketkukade111@gmail.com
   - GMAIL_PASS = (Gmail App Password)

## Gmail App Password कसा मिळवायचा?
1. Google Account → Security → 2-Step Verification enable करा
2. App Passwords → "Mail" + "Windows Computer" → Generate
3. 16 digit password मिळेल → Railway मध्ये GMAIL_PASS म्हणून टाका

## API Endpoints:
- POST /send-alert — HIGH defect alert
- POST /send-onepager — One-pager with PPT attachment
- POST /send-dashboard — Dashboard report
