# 🚀 ConvertRocket - Master Deployment Guide
**Domain:** convertrocket.online

This guide explains EXACTLY how to deploy your app with your custom domain.
Standard web hosts (like Vercel) **cannot** run FFmpeg reliably because of time limits.
**Solution:** We split the app into two parts:
1.  **Frontend (UI):** Hosted on **Vercel** (Fast, connected to `convertrocket.online`)
2.  **Backend (Engine):** Hosted on **Render** (runs Docker/FFmpeg)

---

## 📂 Step 1: Prepare Your Files (ALREADY DONE)

I have already created the necessary config files for you:
1.  **`Dockerfile`**: Tells Render how to install Python & FFmpeg.
2.  **`vercel.json`**: Tells Vercel how to serve your HTML/CSS/JS.
3.  **`main.py`**: Updated to allow requests from `convertrocket.online` (CORS).

---

## 🛠️ Step 2: Deploy Backend (Render.com)
*This runs the "Heavy Lifting" code (Python + FFmpeg).*

1.  **Push to GitHub**:
    *   Upload your entire project code to a GitHub repository (private or public).
2.  **Create Render Account**:
    *   Go to [dashboard.render.com](https://dashboard.render.com) and log in.
3.  **New Web Service**:
    *   Click **"New +"** -> **"Web Service"**.
    *   Select "Build and deploy from a Git repository".
    *   Connect your GitHub repository.
4.  **Configure Service**:
    *   **Name**: `convertrocket-api`
    *   **Region**: Closest to you (e.g., Frankfurt, Singapore, Oregon).
    *   **Runtime**: Select **Docker** (Crucial! Do not select Python).
    *   **Instance Type**: Free (or Starter if you want faster speeds later).
5.  **Environment Variables** (Optional but recommended):
    *   Key: `App_Env`, Value: `production`
6.  **Deploy**:
    *   Click **"Create Web Service"**.
    *   Wait for it to build (it installs FFmpeg + Python).
    *   **COPY THE URL** it gives you (e.g., `https://convertrocket-api.onrender.com`). You need this for Step 3.

---

## 🔗 Step 3: Connect Frontend to Backend

1.  Open the file `frontend/js/app.js` in your code editor.
2.  Find this line at the top (Line 1):
    ```javascript
    const API_BASE = ''; // currently empty
    ```
3.  **Change it** to your new Render URL:
    ```javascript
    const API_BASE = 'https://convertrocket-api.onrender.com'; 
    // ^ Make sure no trailing slash '/'
    ```
4.  Save and commit/push this change to GitHub.

---

## 🌐 Step 4: Deploy Frontend (Vercel)
*This hosts your website at `convertrocket.online`.*

1.  **Vercel Dashboard**:
    *   Go to [vercel.com](https://vercel.com) -> Login.
2.  **Import Project**:
    *   Click **"Add New..."** -> **"Project"**.
    *   Import your GitHub repository.
3.  **Configure Build**:
    *   **Framework Preset**: Select **"Other"**.
    *   **Root Directory**: Leave as `./` (Root).
    *   **Output Directory**: Leave default (config is in `vercel.json`).
4.  **Deploy**:
    *   Click **"Deploy"**.
    *   Wait for the confetti! Your site is live on a `.vercel.app` domain.

---

## 💎 Step 5: Connect Custom Domain
*Point `convertrocket.online` to Vercel.*

1.  **Vercel Settings**:
    *   Go to your Project Dashboard -> **Settings** -> **Domains**.
2.  **Add Domain**:
    *   Type `convertrocket.online`.
    *   Click **Add**.
3.  **DNS Configuration** (Go to where you bought domain, e.g., Namecheap/GoDaddy):
    *   Vercel will show you 2 records to add.
    *   **A Record**:
        *   Host: `@`
        *   Value: `76.76.21.21` (Vercel IP)
    *   **CNAME Record**:
        *   Host: `www`
        *   Value: `cname.vercel-dns.com`
4.  **Wait**: DNS can take 1-24 hours to propagate, but usually works in minutes.

---

## ✅ Deployment Checklist

- [ ] **Backend Live**: Can you visit `https://YOUR-RENDER-URL/api/health` and see `{"status":"healthy"}`?
- [ ] **Frontend Connected**: Does `app.js` point to the Render URL?
- [ ] **Domain Connected**: Does `convertrocket.online` load the site?
- [ ] **Test**: Try converting a PDF to DOCX (checks backend) and converting an image (checks backend).

**Congratulations! Your Universal Converter is live! 🚀**
