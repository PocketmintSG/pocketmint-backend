from io import BytesIO
import boto3

from fastapi import APIRouter, File, UploadFile
from api.models.response_models.common import (
    BaseHTTPException,
    BaseJSONResponse,
    BaseResponseModel,
)
from api.models.response_models.utils import UploadImageResponse
from api.types.requests_types import StatusEnum
from api.utils.file_uploads import (
    compress_image,
    generate_s3_url,
    get_unique_filename,
    validate_image,
)

router = APIRouter()


@router.post("/upload_image", response_model=BaseResponseModel[UploadImageResponse])
async def upload_image(
    image_file: UploadFile = File(...),
):
    image_data = await image_file.read()
    try:
        image_data = await validate_image(image_data)
    except ValueError as e:
        raise BaseHTTPException(
            message="Failure to validate image: " + str(e),
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    try:
        compressed_image_data = await compress_image(image_data)
    except Exception as e:
        raise BaseHTTPException(
            status_code=400,
            message="Failure to compress image: " + str(e),
            status=StatusEnum.FAILURE,
        )

    unique_image_name = get_unique_filename(image_file.filename)
    s3 = boto3.resource("s3")
    s3.Bucket("pocketmint-backend-images").put_object(
        Key=unique_image_name, Body=BytesIO(compressed_image_data)
    )
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Successfully uploaded image!",
        data={
            "image_url": generate_s3_url("pocketmint-backend-images", unique_image_name)
        },
    )
