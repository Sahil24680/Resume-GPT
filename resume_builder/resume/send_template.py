import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def authenticate():
    """Authenticates the user and returns the credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds



def delete_file( file_id):
    """Delete a file by its ID."""
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File with ID: {file_id} deleted successfully.")
    except HttpError as error:
        print(f"An error occurred: {error}")



def list_files(name):
    """Lists all files in Google Drive with the specified name."""
    creds = authenticate()
    try:
        service = build("drive", "v3", credentials=creds)
        query = f"name = '{name}'"
        page_token = None
        while True:
            results = service.files().list(
                q=query,
                spaces='drive',
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()
            items = results.get("files", [])
            
            if not items:
                print("No files found.")
                return
            
            print("Files:")
            for item in items:
                print(item['id'])
                delete_file(item['id'])
            
            page_token = results.get('nextPageToken', None)
            if not page_token:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")




def share_document(document_id, email):
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    # Create permission
    permission = {
        'type': 'user',
        'role': 'writer',  # or 'reader' if you want read-only access
        'emailAddress': email
    }

    try:
        drive_service.permissions().create(
            fileId=document_id,
            body=permission,
            fields='id',
        ).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    else:
        print("sent")

    # Get the shareable link
    try:
        file = drive_service.files().get(fileId=document_id, fields='webViewLink').execute()
        print(file.get('webViewLink'))
        return file.get('webViewLink')
    except HttpError as error:
        print(f"An error occurred while fetching the link: {error}")
        return None
    









if __name__ == "__main__":
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)
    
    recipient_email = 'Suha221209885@gmail.com'
    document_id = "1AZyVSk_3INKs2LRXe0vV1GbHWOaVFl54vy1dLE4Avh0"
   #shareable_link = share_document(document_id, recipient_email)
    #if shareable_link:
        ##else:
       # print("Failed to create a shareable link.")
    