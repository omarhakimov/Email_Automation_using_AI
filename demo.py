#!/usr/bin/env python3
"""
AI Email Automation System - Demo Script

This script demonstrates the main functionality of the email automation system.
Run this after setting up your API keys and Gmail credentials.
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import project modules
try:
    from naive_bayes import preprocess_text
    import pandas as pd
    import joblib
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you've installed all dependencies: pip install -r requirements.txt")
    sys.exit(1)

def setup_logging():
    """Configure logging for the demo"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_requirements():
    """Check if all required files and APIs are configured"""
    checks = []
    
    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    checks.append(("OpenAI API Key", openai_key is not None))
    
    # Check credentials file
    creds_exist = Path('credentials.json').exists()
    checks.append(("Gmail Credentials", creds_exist))
    
    # Check data files
    data_dir = Path('data')
    has_data = data_dir.exists() and any(data_dir.glob('*.xlsx'))
    checks.append(("Email Data", has_data))
    
    # Check model file
    model_exists = Path('label_encoder.pkl').exists()
    checks.append(("Trained Model", model_exists))
    
    print("🔍 System Requirements Check:")
    print("-" * 40)
    
    all_good = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_good = False
    
    print("-" * 40)
    
    if not all_good:
        print("\n⚠️  Some requirements are missing. Please check the setup guide.")
        return False
    
    print("🎉 All requirements satisfied!")
    return True

def demo_text_classification():
    """Demonstrate email classification using the trained model"""
    print("\n📧 Email Classification Demo")
    print("=" * 50)
    
    # Sample emails for testing
    sample_emails = [
        {
            "content": "I need help with my course registration for next semester. Can you guide me through the process?",
            "expected": "Academic"
        },
        {
            "content": "What are the library opening hours during exam period?",
            "expected": "FAQ"
        },
        {
            "content": "I am an international student and need information about work permit renewal.",
            "expected": "WorkPermit"
        }
    ]
    
    try:
        # Load model if it exists
        if Path('label_encoder.pkl').exists():
            print("📁 Loading trained model...")
            # For demo purposes, we'll simulate classification
            for i, email in enumerate(sample_emails, 1):
                print(f"\n📧 Email {i}:")
                print(f"Content: {email['content'][:80]}...")
                print(f"Expected Category: {email['expected']}")
                print(f"Predicted Category: {email['expected']} (Simulated)")
                print(f"Confidence: 0.85 (Simulated)")
        else:
            print("❌ No trained model found. Run naive_bayes.py first to train a model.")
            
    except Exception as e:
        print(f"❌ Error in classification demo: {e}")

def demo_data_processing():
    """Demonstrate data processing capabilities"""
    print("\n📊 Data Processing Demo")
    print("=" * 50)
    
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ Data directory not found")
        return
    
    # List available datasets
    excel_files = list(data_dir.glob('*.xlsx'))
    if not excel_files:
        print("❌ No Excel files found in data directory")
        return
    
    print(f"📂 Found {len(excel_files)} dataset files:")
    for file in excel_files:
        print(f"   • {file.name}")
    
    # Read a sample file
    try:
        sample_file = excel_files[0]
        print(f"\n📖 Reading sample file: {sample_file.name}")
        df = pd.read_excel(sample_file)
        
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        
        if 'Content' in df.columns:
            sample_content = df['Content'].iloc[0] if len(df) > 0 else "No content"
            print(f"   Sample content: {str(sample_content)[:100]}...")
            
    except Exception as e:
        print(f"❌ Error reading data file: {e}")

def demo_text_preprocessing():
    """Demonstrate text preprocessing functionality"""
    print("\n🔤 Text Preprocessing Demo")
    print("=" * 50)
    
    sample_text = "Hello! I need URGENT help with my Grade Appeal Process. Can you help me ASAP? Thanks!!!"
    
    print(f"Original text:")
    print(f"'{sample_text}'")
    
    try:
        # Use the preprocessing function from naive_bayes.py
        cleaned_text = preprocess_text(sample_text)
        print(f"\nProcessed text:")
        print(f"'{cleaned_text}'")
        
        print(f"\nTransformations applied:")
        print("• Converted to lowercase")
        print("• Removed punctuation and numbers")
        print("• Normalized whitespace")
        
    except Exception as e:
        print(f"❌ Error in text preprocessing: {e}")

def main():
    """Main demo function"""
    print("🤖 AI Email Automation System - Demo")
    print("=" * 60)
    
    setup_logging()
    
    # Check system requirements
    if not check_requirements():
        print("\n📚 Setup Instructions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("3. Add Gmail credentials.json file")
        print("4. Train models: python naive_bayes.py")
        print("\nSee README.md for detailed setup instructions.")
        return
    
    # Run demo modules
    demo_data_processing()
    demo_text_preprocessing()
    demo_text_classification()
    
    print("\n🎯 Next Steps:")
    print("1. Train models: python naive_bayes.py")
    print("2. Run Jupyter notebooks: jupyter notebook")
    print("3. Test email processing: python test.py")
    print("4. Start email bot: python email_automation/bot.py")
    
    print("\n📖 Documentation:")
    print("• README.md - Project overview and setup")
    print("• docs/API_SETUP.md - API configuration guide")
    print("• docs/MODEL_GUIDE.md - Model training and evaluation")
    print("• docs/DEPLOYMENT.md - Production deployment guide")

if __name__ == "__main__":
    main()
