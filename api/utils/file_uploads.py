import hashlib
import uuid
import os
import imghdr

from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_REGION = os.environ.get("S3_BUCKET_REGION")


async def compress_image(image_data: bytes, quality: int = 20):
    img = Image.open(BytesIO(image_data))
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True, quality=quality)
    return buffer.getvalue()


async def validate_image(image_data: bytes):
    file_type = imghdr.what(None, h=image_data)
    if not file_type:
        raise ValueError("Uploaded file is not an image")
    return image_data


def generate_s3_url(bucket_name, object_key):
    return f"https://{bucket_name}.s3.{S3_BUCKET_REGION}.amazonaws.com/{object_key}"


def get_unique_filename(file_name: str):
    unique_id = str(uuid.uuid4())
    combined_string = f"{file_name}_{unique_id}"
    hashed_name = hashlib.sha256(combined_string.encode()).hexdigest()
    return hashed_name
