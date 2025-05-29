#1
import os
import pandas as pd

# Path to your folder
folder_path = 'data_filled'

# Combine all files into one DataFrame
all_data = []
for file in os.listdir(folder_path):
    if file.endswith('.xlsx'):  # Check if it's an Excel file
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)
        all_data.append(df)

# Combine all DataFrames
combined_df = pd.concat(all_data, ignore_index=True)
print(combined_df.head())  # Check the first 5 rows

#2

import re

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Apply preprocessing to the "Email Content" column
combined_df['Cleaned_Content'] = combined_df['Content'].apply(preprocess_text)
print(combined_df[['Content', 'Cleaned_Content']].head())


#3


from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=5000)  # Use top 5000 words
X = tfidf.fit_transform(combined_df['Cleaned_Content']).toarray()  # Features
y = combined_df['Category']  # Labels

print("Shape of X:", X.shape)
print("Shape of y:", y.shape)


#4


from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Naïve Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
