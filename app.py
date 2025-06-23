from flask import Flask, request, jsonify
import boto3
import uuid
import os

app = Flask(__name__)

R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ENDPOINT = f"https://{R2_BUCKET}.r2.dev/{filename}"

s3 = boto3.client('s3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
)

@app.route('/')
def index():
    return 'R2 Upload Service Running!'

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"

    # ✅ Log tạm để debug
    print("R2_BUCKET:", R2_BUCKET)
    print("Uploading file:", filename)

    s3.upload_fileobj(file, R2_BUCKET, filename, ExtraArgs={'ACL': 'public-read'})
    url = f"https://{R2_BUCKET}.{R2_ACCOUNT_ID}.r2.cloudflarestorage.com/{filename}"
    return jsonify({'url': url})
