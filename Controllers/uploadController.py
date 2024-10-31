import os
from flask import Flask, jsonify
from flask_restx import Namespace, Resource, reqparse
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import werkzeug
from datetime import datetime, timedelta
from azure.storage.blob import ContentSettings
import uuid  # Import the uuid module for generating random UUIDs
from Domain.extensions import userCollection,menuCollection
from Utils.Exceptions.customExceptions import CustomException
from bson import ObjectId



# Azure Blob Storage account details
ACCOUNT_NAME = "dreamsblob"
ACCOUNT_KEY = "CEpzuG7OcW2sbL5ZU2G9nfcFGN0nCsaVzFa0PpCrABQ6hg7pYczq5kdgKsvy5yMju4qzNixQxrbt+ASttRawbA=="

# Container name
CONTAINER_NAME = "profileimages"
CONTAINER_NAME_FOODPICTURE = "foodimages"

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
    def post(self, email):
        args = upload_parser.parse_args()
        file = args['file']

        # Check if the file is not empty and has an allowed extension
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file'})

        # Find the user by email
        user = userCollection.find_one({"email": email})
        if user is None:
            raise CustomException("User not found", 404)

        # Extract the user's current image URL
        current_image_url = user.get("imageUrl", "")
        default_image_url = "https://dreamsblob.blob.core.windows.net/profileimages/waiters-concept-illustration_114360-2908.avif"

        # Generate a new unique blob name (GUID) for the image
        blob_name = str(uuid.uuid4())

        # If the current image is not the default image, delete the old one
        if current_image_url != default_image_url:
            try:
                # Extract the old image GUID from the current image URL
                old_image_name = current_image_url.split("/")[-1]
                old_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=old_image_name)
                old_blob_client.delete_blob()  # Delete the existing image
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error deleting old image: {str(e)}'})

        # Create a BlobClient for the new image upload with the new GUID
        new_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

        # Upload the new image
        with file.stream as file_stream:
            content_type = get_content_type(file.filename)
            content_settings = ContentSettings(content_type=content_type)
            new_blob_client.upload_blob(data=file_stream, content_settings=content_settings)

        # Construct the URL of the uploaded blob
        blob_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"

        # Update the user's image URL in the database
        userCollection.update_one({"email": email}, {"$set": {"imageUrl": blob_url}})

        return {'success': True, 'message': 'File uploaded successfully', 'url': blob_url}




def deleteImageFromBlob(imageUrl,containerName):
    try:
        # Extract the blob ID from the URL
        blob_id = imageUrl.split('/')[-1]

        # Create a BlobClient pointing to the existing blob
        blob_client = blob_service_client.get_blob_client(container=containerName, blob=blob_id)

        # Check if the blob exists
        if blob_client.exists():
            # Delete the blob
            blob_client.delete_blob()

            # Optionally, update the database or perform any other cleanup
            # userCollection.update_one({"imageUrl": imageUrl}, {"$unset": {"imageUrl": ""}})

            return {'success': True, 'message': 'Image deleted successfully'}
        else:
            return {'success': False, 'message': 'Image not found'}, 404

    except Exception as e:
        return {'success': False, 'message': 'An error occurred while deleting the image', 'error': str(e)}, 500


@nsUpload.route('/uploadimagetoproduct/<string:productId>')
class UploadImageProductResource(Resource):
    @nsUpload.expect(upload_parser)
    def put(self, productId):
        args = upload_parser.parse_args()
        file = args['file']

        # Check if the file is not empty and has an allowed extension
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file'})

        # Find the product by ID
        product = menuCollection.find_one({"_id": ObjectId(productId)})
        if product is None:
            raise CustomException("Product not found", 404)

        # Extract current image URL
        current_image_url = product.get("imageUrl", "")
        default_image_url = "https://dreamsblob.blob.core.windows.net/foodimages/noimage.jpg"

        # Generate a new GUID for the new image's blob name
        blob_name = str(uuid.uuid4())

        # If the current image is not the default image, delete the old image
        if current_image_url != default_image_url:
            try:
                # Extract the old image GUID (last part of the URL)
                current_image_name = current_image_url.split("/")[-1]
                old_blob_client = blob_service_client.get_blob_client(
                    container=CONTAINER_NAME_FOODPICTURE, blob=current_image_name)
                old_blob_client.delete_blob()  # Delete the existing image
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error deleting old image: {str(e)}'})

        # Create a BlobClient for the new image upload
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME_FOODPICTURE, blob=blob_name)

        # Use the BlobClient to upload the file to Azure Blob Storage
        with file.stream as file_stream:
            content_type = get_content_type(file.filename)
            content_settings = ContentSettings(content_type=content_type)
            blob_client.upload_blob(data=file_stream, content_settings=content_settings)

        # Construct the URL of the uploaded blob
        blob_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME_FOODPICTURE}/{blob_name}"

        # Update the product with the new image URL
        menuCollection.update_one({"_id": ObjectId(productId)}, {"$set": {"imageUrl": blob_url}})

        return {'success': True, 'message': 'File uploaded successfully', 'url': blob_url}
