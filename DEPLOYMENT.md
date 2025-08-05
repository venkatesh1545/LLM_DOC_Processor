# Deployment Guide - LLM Document Processor

## Overview
This project has two components that need to be deployed separately:

1. **Frontend Landing Page** - Firebase Hosting (venkatesh7305.me)
2. **Backend API** - FastAPI + Ollama (needs server-side hosting)

---

## Part 1: Firebase Hosting (Landing Page)

### Prerequisites
- Firebase CLI installed: `npm install -g firebase-tools`
- Firebase project created: `LLM-Doc-Processor`
- Custom domain configured: `venkatesh7305.me`

### Deployment Steps

1. **Login to Firebase:**
   ```bash
   firebase login
   ```

2. **Initialize Firebase (if not already done):**
   ```bash
   firebase init hosting
   ```
   - Select your project: `LLM-Doc-Processor`
   - Public directory: `public`
   - Configure as single-page app: `Yes`
   - Overwrite index.html: `No`

3. **Deploy to Firebase:**
   ```bash
   firebase deploy --only hosting
   ```

4. **Verify deployment:**
   - Visit: `https://venkatesh7305.me`
   - Should show the landing page

---

## Part 2: Backend API Deployment (FastAPI + Ollama)

### Option A: AWS EC2 (Recommended)

#### 1. Launch EC2 Instance
- **AMI:** Ubuntu 22.04 LTS
- **Instance Type:** t2.medium or higher (more RAM for Ollama)
- **Storage:** At least 20GB
- **Security Group:** 
  - SSH (22) from your IP
  - HTTP (80) from anywhere
  - HTTPS (443) from anywhere
  - Custom port (8000) for API

#### 2. Connect and Setup
```bash
# SSH to your instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git curl

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

#### 3. Deploy Application
```bash
# Clone your repository
git clone <your-repo-url>
cd llm_doc_processor

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Ollama
ollama serve &
ollama pull llama2  # or your preferred model

# Start FastAPI (in background)
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > app.log 2>&1 &
```

#### 4. Setup Domain and HTTPS (Optional)
```bash
# Install Nginx
sudo apt install nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/llm-doc-processor
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name api.venkatesh7305.me;  # or your API subdomain

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/llm-doc-processor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup HTTPS with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.venkatesh7305.me
```

### Option B: Google Cloud Run (Alternative)

#### 1. Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start Ollama and FastAPI
CMD ["sh", "-c", "ollama serve & sleep 10 && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

#### 2. Deploy to Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/llm-doc-processor

# Deploy to Cloud Run
gcloud run deploy llm-doc-processor \
  --image gcr.io/YOUR_PROJECT_ID/llm-doc-processor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2
```

### Option C: Railway (Alternative)

1. **Connect GitHub repository to Railway**
2. **Set environment variables:**
   - `PORT=8000`
   - `OLLAMA_HOST=0.0.0.0`
3. **Deploy automatically on push**

---

## Part 3: Update Landing Page

After deploying the backend, update the API endpoint in `public/index.html`:

```javascript
// Change this line in the curl example:
'https://your-api-domain.com/api/v1/hackrx/run'
// To your actual API domain:
'https://api.venkatesh7305.me/api/v1/hackrx/run'
```

Then redeploy Firebase:
```bash
firebase deploy --only hosting
```

---

## Part 4: Testing

### Test Landing Page
```bash
curl https://venkatesh7305.me
```

### Test API
```bash
curl -X POST \
  https://api.venkatesh7305.me/api/v1/hackrx/run \
  -H "Authorization: Bearer f54ada5ff8aad823c950caee24b08bafd5d45da70027d16daef3f21f49af01e9" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

---

## Troubleshooting

### Common Issues

1. **Ollama not starting:**
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   
   # Start manually
   ollama serve
   ```

2. **Port conflicts:**
   ```bash
   # Check what's using port 8000
   sudo netstat -tulpn | grep :8000
   ```

3. **Memory issues:**
   - Increase EC2 instance size
   - Use smaller LLM models

4. **Firebase deployment fails:**
   ```bash
   # Clear cache
   firebase logout
   firebase login
   firebase deploy --only hosting
   ```

---

## Security Notes

1. **Change the Bearer token** in production
2. **Use HTTPS** for all API calls
3. **Set up proper firewall rules**
4. **Regular security updates**

---

## Monitoring

### Logs
```bash
# FastAPI logs
tail -f app.log

# Ollama logs
journalctl -u ollama -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
```

### Health Check
```bash
# API health
curl https://api.venkatesh7305.me/

# Ollama health
curl http://localhost:11434/api/tags
``` 