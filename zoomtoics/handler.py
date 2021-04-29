from .zoomtoics import run
import dotenv

def handle(_):
  config = dotenv.dotenv_values("/var/openfaas/secrets/conflictdetector-keys")
  run(
    zoom_api_key=config['ZOOM_API_KEY'],
    zoom_api_secret=config['ZOOM_API_SECRET'],
    webhook_url=config['WEBHOOK_URL'],
    timezone=config['TIMEZONE'],
    s3_region_name=config['S3_REGION_NAME'],
    s3_endpoint_url=config['S3_ENDPOINT_URL'],
    s3_aws_access_key_id=config['S3_AWS_ACCESS_KEY_ID'],
    s3_aws_secret_access_key=config['S3_AWS_SECRET_ACCESS_KEY'],
    s3_bucket=config['S3_BUCKET'],
    s3_output_path=config['S3_OUTPUT_PATH'],
  )
  return '{"status":"ok"}'
