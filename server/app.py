from flask import Flask, request, jsonify, send_from_directory, make_response
from minio import Minio
from minio.error import S3Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure MinIO client
MINIO_ENDPOINT = "192.168.29.127:9000"
MINIO_ACCESS_KEY = "WGQqGhO64LH5wSKOtxHj"
MINIO_SECRET_KEY = "xqkgvQp2pfpmHLxWQuVKMcTSRcTbNYsmOuhB58Kj"
MINIO_BUCKET_NAME = "photos"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Set the bucket name where you want to store the uploaded files
bucket_name = MINIO_BUCKET_NAME

@app.route('/photos', methods=['GET'])
def get_photos():
    try:
        photos = [obj.object_name for obj in minio_client.list_objects(bucket_name, recursive=True)]
        return jsonify(photos)
    except S3Error as e:
        return jsonify({"error": str(e)})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"})

        # Calculate content length
        file.seek(0, 2)  # Move to the end of the file
        content_length = file.tell()
        file.seek(0)  # Reset file position

        minio_client.put_object(bucket_name, file.filename, file, content_length)
        return jsonify({"message": "File uploaded successfully!"})
    except S3Error as e:
        return jsonify({"error": str(e)})

@app.route('/photos/<filename>', methods=['GET'])
def serve_photo(filename):
    try:
        response = make_response(minio_client.get_object(bucket_name, filename).read())
        response.headers["Content-Type"] = "image/jpeg"  # Change to the appropriate content type
        return response
    except S3Error as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
