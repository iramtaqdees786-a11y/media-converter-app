# 🚀 Deployment Guide: ConvertRocket (Frontend + Backend)

This guide explains how to deploy **ConvertRocket** properly. Since this app requires heavy media processing (FFmpeg), standard Vercel functions often time out (max 10s-60s limit).

**The Best Strategy:**
1. **Frontend (UI)** → Hosted on **Vercel** (Fast, Global CDN)
2. **Backend (API + FFmpeg)** → Hosted on **Render.com** (Supports Docker + FFmpeg)

---

## Part 1: Deploy Backend (The Engine) on Render.com

Render is perfect because it supports Docker, meaning we can install FFmpeg easily.

### 1. Preparation
Create a `Dockerfile` in your project root if it doesn't exist:

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install system dependencies including FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```

### 2. Deploy to Render
1. Push your code to **GitHub**.
2. Go to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository.
5. Select **Docker** as the Runtime.
6. Click **Create Web Service**.

Render will build your app, install FFmpeg automatically via the Dockerfile, and give you a URL (e.g., `https://convertrocket-api.onrender.com`).

---

## Part 2: Deploy Frontend on Vercel

### 1. Update Frontend API Link
Before deploying, we need the frontend to talk to your new Render Backend instead of `localhost`.

Open `frontend/js/app.js` and change:
```javascript
// BEFORE
const API_BASE = ''; 

// AFTER (Replace with your actual Render URL)
const API_BASE = 'https://convertrocket-api.onrender.com';
```

### 2. Configure for Vercel
Create a file named `vercel.json` in the project root to serve the `frontend` folder as a static site:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

### 3. Deploy
1. Push the changes to GitHub.
2. Go to [vercel.com](https://vercel.com).
3. **Add New Project** → Import your repo.
4. **Build Settings**:
   - Framework Preset: **Other**
   - Output Directory: `frontend` (or leave default if using the vercel.json method above)
5. Click **Deploy**.

---

## Part 3: Custom Domain Setup (convertrocket.online)

You want your domain `convertrocket.online` to point to the Vercel frontend.

1.  **Vercel Dashboard** → Go to your Project → **Settings** → **Domains**.
2.  Enter `convertrocket.online`.
3.  Vercel will give you DNS records (A Record or CNAME).
4.  **Go to your Domain Registrar** (e.g., Namecheap, GoDaddy).
5.  Add the records Vercel provided:
    *   **Type**: `A`
    *   **Name**: `@`
    *   **Value**: `76.76.21.21` (Vercel IP)
    *   **Type**: `CNAME`
    *   **Name**: `www`
    *   **Value**: `cname.vercel-dns.com`

**Result:**
*   User visits `convertrocket.online` → Hits Vercel (Frontend).
*   User uploads file → Vercel sends request to Render (Backend).
*   Render converts file using FFmpeg and returns result.

---

## ⚠️ Important Note on "Same Origin"
Since Frontend and Backend are on different domains (Vercel vs Render), you must enable **CORS** in your backend `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://convertrocket.online", "https://www.convertrocket.online"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Done! 🚀**
