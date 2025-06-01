# Deployment Guide

This guide covers deploying the AI Email Automation System in production environments.

## 🚀 Deployment Options

### 1. Local Development Server
**Best for**: Testing, development, small-scale usage

```bash
# Activate environment
source venv/bin/activate

# Run email processing
python test.py

# Run email bot
python email_automation/bot.py
```

### 2. Cloud Server Deployment
**Best for**: Production use, scalability, 24/7 operation

#### AWS EC2 Deployment
```bash
# 1. Launch EC2 instance (t3.medium or larger)
# 2. Install dependencies
sudo apt update
sudo apt install python3 python3-pip git

# 3. Clone repository
git clone <your-repo-url>
cd ai_email_automation

# 4. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment variables
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"

# 6. Setup systemd service (see below)
```

#### Google Cloud Platform
```bash
# Deploy to Google Cloud Run
gcloud run deploy email-automation \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
# Create container image
docker build -t email-automation .

# Deploy to Azure
az container create \
  --resource-group myResourceGroup \
  --name email-automation \
  --image email-automation
```

### 3. Docker Deployment
**Best for**: Containerized environments, consistent deployments

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "email_automation/bot.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  email-automation:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./credentials.json:/app/credentials.json
      - ./data:/app/data
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

## ⚙️ Production Configuration

### 1. Environment Variables
Create production `.env` file:
```bash
# Production environment variables
OPENAI_API_KEY=prod-openai-key
DEEPSEEK_API_KEY=prod-deepseek-key
EMAIL_CHECK_INTERVAL=300  # 5 minutes
MAX_EMAILS_PER_BATCH=10
LOG_LEVEL=INFO
SMTP_SERVER=smtp.gmail.com
IMAP_SERVER=imap.gmail.com
```

### 2. Logging Configuration
Create `logging_config.py`:
```python
import logging
import logging.handlers
import os

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                'logs/email_automation.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

### 3. Error Handling and Retry Logic
```python
import time
import logging
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        logging.error(f"All {max_retries} attempts failed")
                        raise
            return wrapper
        return decorator

# Usage
@retry_on_failure(max_retries=3)
def process_email(email_content):
    # Email processing logic
    pass
```

## 🔒 Security Considerations

### 1. API Key Management
```bash
# Use AWS Systems Manager Parameter Store
aws ssm put-parameter \
  --name "/email-automation/openai-key" \
  --value "your-openai-key" \
  --type "SecureString"

# Retrieve in application
import boto3
ssm = boto3.client('ssm')
response = ssm.get_parameter(
    Name='/email-automation/openai-key',
    WithDecryption=True
)
openai_key = response['Parameter']['Value']
```

### 2. Network Security
- Use HTTPS/TLS for all API communications
- Implement IP whitelisting if possible
- Use VPC for cloud deployments
- Regular security updates

### 3. Data Protection
```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

def encrypt_email_content(content, key):
    f = Fernet(key)
    encrypted_content = f.encrypt(content.encode())
    return encrypted_content

def decrypt_email_content(encrypted_content, key):
    f = Fernet(key)
    decrypted_content = f.decrypt(encrypted_content)
    return decrypted_content.decode()
```

## 📊 Monitoring and Alerting

### 1. Health Checks
```python
# health_check.py
import requests
from datetime import datetime

def health_check():
    checks = {
        'openai_api': check_openai_api(),
        'gmail_api': check_gmail_api(),
        'disk_space': check_disk_space(),
        'memory_usage': check_memory_usage()
    }
    
    all_healthy = all(checks.values())
    
    return {
        'status': 'healthy' if all_healthy else 'unhealthy',
        'timestamp': datetime.now().isoformat(),
        'checks': checks
    }

def check_openai_api():
    try:
        # Simple API test
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        return True
    except:
        return False
```

### 2. Metrics Collection
```python
# metrics.py
import time
import logging
from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def record_processing_time(self, email_type, processing_time):
        self.metrics[f'processing_time_{email_type}'].append(processing_time)
    
    def record_classification_accuracy(self, accuracy):
        self.metrics['classification_accuracy'].append(accuracy)
    
    def record_api_response_time(self, api_name, response_time):
        self.metrics[f'api_response_time_{api_name}'].append(response_time)
    
    def get_summary(self):
        summary = {}
        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    'count': len(values),
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                }
        return summary
```

### 3. Alerting System
```python
# alerts.py
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message, recipients):
    try:
        msg = MIMEText(message)
        msg['Subject'] = f"[EMAIL-AUTOMATION ALERT] {subject}"
        msg['From'] = "alerts@yourdomain.com"
        msg['To'] = ", ".join(recipients)
        
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
            
        logging.info(f"Alert sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

# Usage
def check_and_alert():
    health = health_check()
    if health['status'] == 'unhealthy':
        send_alert(
            "System Health Check Failed",
            f"Health check failed at {health['timestamp']}\n"
            f"Failed checks: {health['checks']}",
            ["admin@yourdomain.com"]
        )
```

## 🔄 Continuous Deployment

### 1. GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to server
      run: |
        # SSH and deploy commands
        ssh user@server 'cd /app && git pull && systemctl restart email-automation'
```

### 2. Blue-Green Deployment
```bash
# Deploy new version alongside current
docker run -d --name email-automation-green \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  email-automation:latest

# Test new version
curl http://localhost:8081/health

# Switch traffic (update load balancer)
# Stop old version
docker stop email-automation-blue
docker rm email-automation-blue
```

## 📈 Scaling Considerations

### 1. Horizontal Scaling
- Deploy multiple instances
- Use load balancer for distribution
- Implement message queue for email processing
- Database for shared state

### 2. Performance Optimization
```python
# Use connection pooling
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Use async processing for I/O operations
import asyncio
import aiohttp

async def process_emails_async(emails):
    async with aiohttp.ClientSession() as session:
        tasks = [process_single_email(session, email) for email in emails]
        results = await asyncio.gather(*tasks)
    return results
```

## 🛠️ Maintenance

### 1. Regular Tasks
- Monitor API usage and costs
- Update dependencies monthly
- Backup model files and configurations
- Review and rotate API keys quarterly
- Monitor system performance metrics

### 2. Troubleshooting
```bash
# Check application logs
tail -f logs/email_automation.log

# Check system resources
htop
df -h
free -m

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Restart services
systemctl restart email-automation
systemctl status email-automation
```

### 3. Backup Strategy
```bash
# Backup model files
tar -czf backup-$(date +%Y%m%d).tar.gz \
  *.pkl data/ email_automation/

# Upload to cloud storage
aws s3 cp backup-$(date +%Y%m%d).tar.gz \
  s3://your-backup-bucket/
```
