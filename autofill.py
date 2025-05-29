import pandas as pd
import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store the key in an environment variable

# Load the Excel file
input_file = "./data/emailsAcademic.xlsx"
output_file = "./data_filled/emailsAcademic.xlsx"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Ensure column names are clean and maintain proper case
df.columns = df.columns.str.strip()

# Ensure required columns exist
required_columns = ["Subject", "Content", "Answer"]
for col in required_columns:
    if col not in df.columns:
        df[col] = ""  # Add missing columns with empty values

# Convert columns to string type and replace NaN with empty strings
df["Subject"] = df["Subject"].fillna("").astype(str)
df["Content"] = df["Content"].fillna("").astype(str)
df["Answer"] = df["Answer"].fillna("").astype(str)

def generate_response(prompt):
    """Helper function to generate responses from OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Correct model name
            messages=[{"role": "user", "content": prompt}]
        )
        generated_text = response["choices"][0]["message"]["content"].strip()
        print(f"Generated Response: {generated_text}")
        return generated_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Iterate through rows and generate missing content or answers
if not df.empty:
    for index, row in df.iterrows():
        subject = str(row.get("Subject", "")).strip()
        content = str(row.get("Content", "")).strip()
        answer = str(row.get("Answer", "")).strip()

        if pd.isna(content) or content.strip() == "":
            prompt = (f"You are an AI trained to generate professional and concise university-related emails. "
                      f"Given the subject: '{subject}', write a formal email relevant to it. "
                      f"Do not add any extra text—only the email body. Do not make it even look like it is AI generated. Try to improvise if needed.")

            response = generate_response(prompt)
            if response:
                df.at[index, "Content"] = response
        elif pd.isna(answer) or answer.strip() == "" or answer.strip().lower() == "nan":
            prompt = (f"You are an AI trained to provide clear and concise answers for a university FAQ database. "
                      f"Given the subject '{subject}' and content '{content}', write a professional response. "
                      f"Do not include unnecessary words or formatting — only the direct answer. Do not make it even look like it is AI generated. Try to improvise if needed.")

            response = generate_response(prompt)
            if response:
                df.at[index, "Answer"] = response

# Save the updated file
df.to_excel(output_file, index=False)

print(f"File saved: {output_file}")
