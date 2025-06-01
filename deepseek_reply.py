import openai
import joblib
from transformers import pipeline
import pandas as pd

openai.api_base = "https://api.deepseek.com/v1"
openai.api_key = "sk-2448df6a620d47d5aaa07efdbf3d8de6"



# Load Naïve Bayes/SVM
nb_model = joblib.load('label_encoder.pkl')



# Load your knowledge base
kb_df = pd.read_excel('university_kb.xlsx')  # Columns: [Category, Question, Answer]

def generate_response(email_text, confidence_threshold=0.8):
    # 1. Classify email
    nb_features = vectorizer.transform([email_text])
    nb_pred = nb_model.predict(nb_features)[0]
    nb_proba = nb_model.predict_proba(nb_features).max()

    bert_pred = bert_classifier(email_text)[0]

    # 2. Consensus prediction
    final_category = nb_pred if nb_proba > confidence_threshold else bert_pred['label']

    # 3. Retrieve template answer
    template = kb_df[kb_df['Category'] == final_category].sample(1)['Answer'].values[0]

    # 4. Enhance with AI (only if needed)
    if "[AI_GENERATE]" in template:
        prompt = f"""As a university advisor, reply to this email about {final_category}:
        Email: {email_text}
        Base Response: {template.replace('[AI_GENERATE]','')}
        Improved Response:"""

        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # Keep it factual
        )
        return response.choices[0].message.content
    else:
        return template
