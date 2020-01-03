export PROJECT="GCP_PROJECT_NAME"
export TOPIC="GCP_PUB/SUB_TOPIC_NAME"
export BUCKET="GCP_STORAGE_PATH"
python pipeline_stream.py --runner DataFlow --project $PROJECT --temp_location $BUCKET/tmp --staging_location $BUCKET/staging --streaming
