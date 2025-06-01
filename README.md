# AI Email Automation System

A comprehensive machine learning-powered email automation system designed for university email management. This project implements multiple ML approaches for email classification and automated response generation using OpenAI GPT, Gmail API integration, and various transformer models.

## 🚀 Features

- **Multi-Model Email Classification**: Implements three different ML approaches:
  - Naive Bayes with TF-IDF vectorization
  - DistilBERT transformer model
  - RoBERTa fine-tuned model
- **Automated Email Processing**: Gmail API integration for reading and responding to emails
- **AI-Powered Response Generation**: Uses OpenAI GPT and DeepSeek APIs for intelligent email replies
- **Category-Specific Processing**: Handles Academic, FAQ, and Work Permit email categories
- **Data Preprocessing Pipeline**: Automated data cleaning and augmentation workflows

## 📁 Project Structure

```
ai_email_automation/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── setup.sh                    # Automated setup script
├── demo.py                     # Demo script to test functionality
├── .gitignore                  # Git ignore rules
├── label_encoder.pkl           # Trained label encoder model
│
├── 📊 Machine Learning Models
│   ├── bert.ipynb             # DistilBERT email classification notebook
│   ├── RoBERTa_Project.ipynb  # RoBERTa model training and evaluation
│   ├── draft.ipynb            # Naive Bayes classification experiments
│   └── naive_bayes.py         # Naive Bayes implementation script
│
├── 🤖 Email Automation Scripts
│   ├── autofill.py            # OpenAI-based email content generation
│   ├── deepseek_reply.py      # DeepSeek API integration for responses
│   ├── test.py                # Gmail API integration and email processing
│   └── email_automation/
│       └── bot.py             # Main email bot implementation
│
├── 📂 Data Directories
│   ├── data/                  # Original datasets
│   │   ├── emailsAcademic.xlsx    # Academic email dataset
│   │   ├── emailsFAQ.xlsx         # FAQ email dataset
│   │   ├── emailsWorkPermit.xlsx  # Work permit email dataset
│   │   ├── AcademicQA.xlsx        # Academic Q&A pairs
│   │   ├── FAQs_scraped.xlsx      # Scraped FAQ data
│   │   ├── WorkPermitQA.xlsx      # Work permit Q&A pairs
│   │   └── new.xlsx               # Additional dataset
│   └── data_filled/           # AI-processed datasets with generated content
│       ├── emailsAcademic.xlsx
│       ├── emailsFAQ.xlsx
│       ├── emailsWorkPermit.xlsx
│       └── FAQs_scraped.xlsx
│
└── 📚 Documentation
    ├── API_SETUP.md           # API configuration guide
    ├── MODEL_GUIDE.md         # Model training and evaluation
    └── DEPLOYMENT.md          # Production deployment guide
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Gmail account with API access enabled
- OpenAI API key
- DeepSeek API key (optional)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_email_automation
   ```

2. **Quick Setup (Recommended)**
   ```bash
   ./setup.sh
   ```

3. **Manual Setup**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DEEPSEEK_API_KEY="your-deepseek-api-key"  # Optional
   ```

5. **Configure Gmail API**
   - Follow the detailed guide in [`docs/API_SETUP.md`](docs/API_SETUP.md)
   - Download `credentials.json` and place it in the project root

6. **Test your setup**
   ```bash
   python demo.py
   ```

## 🚀 Usage

### 1. Data Preprocessing and Model Training

**Train Naive Bayes Model:**
```bash
python naive_bayes.py
```

**Run Jupyter Notebooks for Advanced Models:**
```bash
# Start Jupyter
jupyter notebook

# Open and run:
# - bert.ipynb for DistilBERT model
# - RoBERTa_Project.ipynb for RoBERTa model
# - draft.ipynb for experimentation
```

### 2. Email Content Generation

**Generate AI responses for existing datasets:**
```bash
python autofill.py
```

### 3. Email Automation

**Process Gmail inbox:**
```bash
python test.py
```

**Run the email bot:**
```bash
python email_automation/bot.py
```

**Generate responses using DeepSeek API:**
```bash
python deepseek_reply.py
```

## 🤖 Machine Learning Models

### 1. Naive Bayes Classifier
- **File**: `naive_bayes.py`
- **Features**: TF-IDF vectorization with 5000 features
- **Preprocessing**: Text cleaning, punctuation removal, case normalization
- **Performance**: Fast training and inference, suitable for real-time classification

### 2. DistilBERT Model
- **File**: `bert.ipynb`
- **Type**: Pre-trained transformer model fine-tuned for email classification
- **Advantages**: Better context understanding, higher accuracy
- **Use Case**: More accurate classification for complex email content

### 3. RoBERTa Model
- **File**: `RoBERTa_Project.ipynb`
- **Type**: Advanced transformer model with robust training
- **Performance**: Highest accuracy for email classification tasks
- **Training**: Comprehensive fine-tuning on email datasets

## 📊 Email Categories

The system handles three main email categories:

1. **Academic**: Course-related inquiries, grading questions, academic procedures
2. **FAQ**: Frequently asked questions about university services
3. **Work Permit**: International student work authorization queries

## 🔧 Configuration

### Email Bot Configuration
Edit `email_automation/bot.py` to configure:
- SMTP/IMAP server settings
- Email credentials
- API keys
- Response templates

### API Integration
- **OpenAI GPT**: Used in `autofill.py` for content generation
- **DeepSeek**: Alternative API for response generation in `deepseek_reply.py`
- **Gmail API**: Email reading and sending functionality in `test.py`

## 📈 Performance Metrics

The project includes comprehensive evaluation metrics:
- Classification accuracy
- Precision and recall for each category
- F1-scores
- Confusion matrices
- Response quality assessment

## 📚 Documentation

- **[API Setup Guide](docs/API_SETUP.md)** - Detailed configuration for OpenAI, Gmail, and DeepSeek APIs
- **[Model Training Guide](docs/MODEL_GUIDE.md)** - Comprehensive guide to training and evaluating ML models
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment and scaling instructions

## 🧪 Quick Demo

Run the demo script to test your setup and see the system in action:

```bash
python demo.py
```

This will:
- Check your configuration
- Demonstrate text preprocessing
- Show data processing capabilities
- Test email classification (if models are trained)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of a graduation project and is intended for educational purposes.