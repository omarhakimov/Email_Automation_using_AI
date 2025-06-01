# API Configuration Guide

This guide helps you set up the required API keys and configurations for the AI Email Automation System.

## 🔑 Required API Keys

### 1. OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and set it as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Cost Considerations:**
- OpenAI API usage is pay-per-use
- Email generation typically costs $0.01-0.05 per email
- Monitor usage in OpenAI dashboard

### 2. Gmail API Setup

#### Step 1: Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2: Create Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Choose "Desktop Application"
4. Download the JSON file and rename it to `credentials.json`
5. Place it in the project root directory

#### Step 3: Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - Application name: "AI Email Automation"
   - User support email: your email
   - Developer contact: your email
4. Add scopes: `https://www.googleapis.com/auth/gmail.modify`
5. Add test users (your email address)

### 3. DeepSeek API (Optional)

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and get API key
3. Set environment variable:

```bash
export DEEPSEEK_API_KEY="your-deepseek-api-key-here"
```

## 🔒 Security Best Practices

### Environment Variables
Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your-openai-api-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key-here
GMAIL_CREDENTIALS_PATH=./credentials.json
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')
```

### Credential Storage
- **Never** commit API keys to version control
- Use environment variables or encrypted credential stores
- Rotate API keys regularly
- Monitor API usage for unauthorized access

## 📧 Email Configuration

### SMTP/IMAP Settings
For Gmail integration, use these settings:

```python
# Gmail SMTP/IMAP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
```

### App Passwords (Alternative to OAuth)
If using app passwords instead of OAuth:

1. Enable 2-factor authentication on Gmail
2. Generate an app password:
   - Go to Google Account settings
   - Security > 2-Step Verification
   - App passwords > Generate password
3. Use this password instead of your regular Gmail password

## 🧪 Testing Configuration

### Test with Limited Scope
1. Start with a test Gmail account
2. Use read-only permissions initially
3. Test with a small dataset
4. Monitor API costs during development

### Validation Script
Create a simple test to validate your setup:

```python
# test_config.py
import os
import openai
from google.oauth2.credentials import Credentials

def test_openai():
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI API working")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_gmail():
    try:
        # Test if credentials.json exists
        if os.path.exists('credentials.json'):
            print("✅ Gmail credentials file found")
            return True
        else:
            print("❌ credentials.json not found")
            return False
    except Exception as e:
        print(f"❌ Gmail setup error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API Configuration...")
    openai_ok = test_openai()
    gmail_ok = test_gmail()
    
    if openai_ok and gmail_ok:
        print("🎉 All APIs configured correctly!")
    else:
        print("⚠️  Some APIs need configuration")
```

## 📞 Troubleshooting

### Common Issues

**"Invalid API Key" Error:**
- Check if API key is correctly set
- Verify no extra spaces or characters
- Ensure environment variable is loaded

**Gmail Authentication Failed:**
- Check credentials.json is in correct location
- Verify OAuth consent screen is configured
- Make sure Gmail API is enabled

**Rate Limiting:**
- OpenAI: Respect rate limits (varies by plan)
- Gmail: Max 1 billion quota units per day
- Implement exponential backoff for retries

**Permission Denied:**
- Check OAuth scopes are correctly configured
- Verify user has granted necessary permissions
- Test with a different Gmail account
