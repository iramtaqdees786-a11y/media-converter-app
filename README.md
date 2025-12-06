# ConvertRocket - Universal Converter & All-Platform Downloader

🚀 **Live Domain:** convertrocket.online

## Features

✨ **ALL-IN-ONE CONVERTER**
- 100% Privacy - Files never stored
- 10x Speed - Lightning fast processing
- Forever Free - No signup needed
- No Limits - Unlimited conversions
- HD Quality - Best output
- Works Globally - Available worldwide

## Supported Conversions

### ✅ Working Formats

#### Documents
- PDF ↔ DOCX ↔ TXT
- Full text extraction and conversion

#### Spreadsheets
- XLSX ↔ XLS ↔ CSV
- Perfect for data conversion

#### Images (via Pillow)
- JPG/JPEG, PNG, WebP, GIF, BMP
- All image formats fully supported

### ⚠️ FFmpeg-Dependent (Requires FFmpeg Installation)

#### Video
- MP4, MOV, MKV, WebM, AVI
- **Requires FFmpeg** to be installed

#### Audio
- MP3, WAV, AAC, OGG, FLAC
- **Requires FFmpeg** to be installed

## Installation

### Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (for video/audio conversions)

### FFmpeg Installation

#### Windows
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH after installation
```

#### Mac
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

### Application Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python main.py
```

3. **Access the App**
- Local: http://localhost:8000
- Production: https://convertrocket.online

## File Locations

- **Downloads**: `~/Downloads/ConvertRocket/`
- **Uploads**: `./uploads/`
- **Converted Files**: `./converted/`

## Deployment

### Production Checklist

- [x] All document conversions working
- [x] All spreadsheet conversions working
- [x] All image conversions working (Pillow)
- [ ] FFmpeg installed on server (for video/audio)
- [x] Downloads go to user's Downloads folder
- [x] Error messages are user-friendly
- [x] SEO optimized with meta tags
- [x] Multi-language support (17+ languages)
- [x] Mobile responsive
- [x] Share button copies URL

### Server Requirements

**Minimum:**
- Python 3.8+
- 2GB RAM
- 10GB Storage
- FFmpeg (for video/audio)

**Recommended:**
- Python 3.10+
- 4GB RAM
- 50GB Storage
- FFmpeg with all codecs

### Environment Variables

```bash
# Optional
FFMPEG_PATH=/usr/bin/ffmpeg  # Custom FFmpeg path
MAX_FILE_SIZE=500  # Max file size in MB
```

## API Documentation

Access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Video/Audio Conversions Not Working

**Cause:** FFmpeg not installed or not in PATH

**Solution:**
1. Install FFmpeg (see instructions above)
2. Verify installation: `ffmpeg -version`
3. Ensure FFmpeg is in system PATH

### Image Conversions Failing

**Cause:** Pillow installation issue

**Solution:**
```bash
pip uninstall Pillow
pip install --upgrade Pillow
```

### Downloads Not Appearing

**Cause:** Permission issues

**Solution:**
- Check `~/Downloads/ConvertRocket/` folder exists
- Ensure write permissions

## Production Deployment (Render/Heroku/AWS)

### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: convertrocket
    env: python
    buildCommand: pip install -r requirements.txt && apt-get update && apt-get install -y ffmpeg
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Heroku
```
# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Add buildpack
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```

### Docker
```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security

- Files auto-deleted after processing
- No user tracking
- HTTPS enforced
- Input validation on all uploads
- File size limits enforced

## License

MIT License - Free for all use

## Support

- Domain: convertrocket.online
- Email: support@convertrocket.online

---

**Made with ❤️ for free universal file conversion**
