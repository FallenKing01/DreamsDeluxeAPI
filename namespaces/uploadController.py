import os
from flask import Flask, jsonify
from flask_restx import Namespace, Resource, reqparse
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import werkzeug
from datetime import datetime, timedelta
from azure.storage.blob import ContentSettings
import uuid  # Import the uuid module for generating random UUIDs
from extensions import db
from bson import ObjectId

userCollection = db["user"]


# Azure Blob Storage account details
ACCOUNT_NAME = "dreamsblob"
ACCOUNT_KEY = "CEpzuG7OcW2sbL5ZU2G9nfcFGN0nCsaVzFa0PpCrABQ6hg7pYczq5kdgKsvy5yMju4qzNixQxrbt+ASttRawbA=="

# Container name
CONTAINER_NAME = "profileimages"

# Create a BlobServiceClient with the account details
blob_service_client = BlobServiceClient(account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
                                       credential=ACCOUNT_KEY)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

nsUpload = Namespace("upload", description="Upload data")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=werkzeug.datastructures.FileStorage, required=True, help='File upload')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_content_type(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension == '.jpg' or extension == '.jpeg':
        return 'image/jpeg'
    elif extension == '.png':
        return 'image/png'
    elif extension == '.gif':
        return 'image/gif'
    else:
        return 'application/octet-stream' 

@nsUpload.route('/upload_image/<string:email>')
class UploadImageResource(Resource):
    @nsUpload.expect(upload_parser)
    def post(self,email):
        args = upload_parser.parse_args()
        file = args['file']

        # Check if the file is not empty and has an allowed extension
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file'})

        # Generate a random UUID string for the blob name
        blob_name = str(uuid.uuid4())

        # Create a BlobClient without specifying blob_name initially
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

        # Use the BlobClient to upload the file to Azure Blob Storage
        with file.stream as file_stream:
            # Get content type based on file extension
            content_type = get_content_type(file.filename)

            # Create an instance of ContentSettings
            content_settings = ContentSettings(content_type=content_type)

            # Upload the file with the generated blob name and specified content type
            blob_client.upload_blob(data=file_stream, content_settings=content_settings)

        # Construct the URL of the uploaded blob
        blob_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        user = userCollection.find_one({"email": email})
        if user is None:
            abort(404, "User not found")

        userCollection.update_one({"email": email}, {"$set": {"imageUrl": blob_url}})

        return {'success': True, 'message': 'File uploaded successfully', 'url': blob_url}
