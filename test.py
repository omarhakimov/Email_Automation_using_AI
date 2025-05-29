import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    for msg in messages:
        msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        msg_str = base64.urlsafe_b64decode(msg['payload']['body']['data'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)
        print(mime_msg.get_payload())
        # Process email content
        process_email(mime_msg)

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)

def process_email(mime_msg):
    # Extract email content and sender
    email_text = mime_msg.get_payload()
    sender = mime_msg['from']

    # Use NLP to classify and generate response
    intent = classify_intent(email_text)
    response = generate_response(intent)

    # Send response email
    email_message = create_message('me', sender, 'Re: ' + mime_msg['subject'], response)
    send_message(get_service(), 'me', email_message)

def classify_intent(email_text):
    candidate_labels = ["work_permit", "activities", "documents", "course_information", "enrollment_procedures", "tuition_fees", "housing"]
    result = classifier(email_text, candidate_labels)
    return result['labels'][0]  # Return the top intent

def generate_response(intent):
    # Simplified response generation
    return knowledge_base.get(intent, {}).get("general", "I'm not sure how to help with that.")

# Periodically check for new emails
service = get_service()
get_emails(service)
