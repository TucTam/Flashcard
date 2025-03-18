import os
from werkzeug.utils import secure_filename
from flask import current_app, redirect, request

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    """
    if not filename or "." not in filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]

def validate_image_and_upload(file, foldername):
    """Validates image uploads by checking if the extensions and filenames are safe and uploads them to the database uploads folder.

    Args:
        file (werkzeug.datastructures.FileStorage): The uploaded file from request.files['file'].

    Returns:
        string: Secure filename if valid, otherwise None.
    """
    # Ensure file exists
    if file is None or file.filename == "":
        return None  # No file uploaded

    # Check if the file extension is allowed
    if not allowed_file(file.filename):
        return None  # Invalid file extension

    # Secure the filename
    filename = secure_filename(file.filename)

    # Verify file size (limit to 5MB)
    file.seek(0, os.SEEK_END)  # Move to end of file
    file_length = file.tell()  # Get file size
    file.seek(0)  # Reset file pointer

    max_size = current_app.config.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)  # Default 5MB
    if file_length > max_size:
        return None  # File too large

    # Verify MIME type
    if file.mimetype not in current_app.config["ALLOWED_IMAGE_MIME_TYPES"]:
        return None  # Invalid MIME type

    # Save the file securely
    child_foldername = foldername
    folder_path = os.path.join(current_app.config["UPLOAD_FOLDER"] , child_foldername)
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, filename)
    print("File is saved")
    try:
        file.save(save_path)
    except Exception as e:
        current_app.logger.error(f"File save error: {e}")
        return None  # Failed to save

    return filename  # Return the saved filename
