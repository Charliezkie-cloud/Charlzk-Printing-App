import tkinter as tk
from tkinter import filedialog, messagebox

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

import os

folder_id = "1ucuhuXX7FYH2MUSLnFavJG-mTp449L2H"
crendtials_path = "./credentials.json"

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(
    crendtials_path, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)


def upload_file_to_folder(file_path, file_name, folder_id):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    try:
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata,
                                      media_body=media, fields='id').execute()

        print(f"File uploaded with ID: {file.get('id')}")
        return file.get('id')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def select_file():
    file_paths = filedialog.askopenfilenames(
        title="Select a file(s) to print...",
        filetypes=[
            ("Text and Documents",
             "*.txt *.rtf *.doc *.docx *.xls *.xlsx *.pdf *.odt *.ods *.md"),
            ("Presentations", "*.ppt *.pptx *.odp"),
            ("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.svg"),
            ("Other Printable Files", "*.csv *.html *.htm *.epub *.mobi")
        ]
    )

    if not file_paths:
        return

    messagebox.showinfo(
        title="Charlzk Printing App Notification",
        message="Your files are currently being uploaded. Please wait.")

    for path in file_paths:
        file_name = os.path.basename(path)
        response = is_copy(folder_id, file_name)

        if not response:
            upload_file_to_folder(path, file_name, folder_id)

    messagebox.showinfo(title="Charlzk Printing App Notification",
                        message="Your files have been successfully uploaded. Please inform the owner to proceed with printing the files.")


def is_copy(folder_id, filename):
    query = f"'{folder_id}' in parents and trashed = false"

    results = service.files().list(
        q=query,
        fields="files(id, name)"
    ).execute()

    items = results.get('files', [])

    if items:
        for item in items:
            name = item["name"]

            if filename == name:
                response = messagebox.askyesno(title="Charlzk Printing App Notification",
                                               message=f'{name} has already been uploaded. Would you like to proceed with uploading it again?')
                if not response:
                    return True


root = tk.Tk()
root.attributes("-topmost", True)
root.withdraw()

select_file()
