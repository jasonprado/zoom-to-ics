#!/usr/bin/env python3
"""Gathers Zoom meetings and renders them into an ICS file.
"""

from pprint import pprint
from ics import Calendar, Event
import collections
import json
import os
from zoomus import ZoomClient
from dateutil import tz
from datetime import datetime, timedelta
import boto3
import tempfile


Meeting = collections.namedtuple('Meeting', ['id', 'title', 'start_time', 'end_time'])


def run(
  zoom_api_key,
  zoom_api_secret,
  timezone,
  s3_region_name,
  s3_endpoint_url,
  s3_aws_access_key_id,
  s3_aws_secret_access_key,
  s3_bucket,
  s3_output_path,
):
  print('Starting')
  timezone = tz.gettz(timezone)
  client = ZoomClient(zoom_api_key, zoom_api_secret)

  user_list_response = client.user.list()
  user_list = json.loads(user_list_response.content)

  ics_calendar = Calendar()

  for user in user_list['users']:
    user_id = user['id']
    meetings = json.loads(client.meeting.list(user_id=user_id, type='upcoming', page_size=300).content)['meetings']
    for meeting in meetings:
      if not meeting.get('start_time'):
        continue
      e = Event(
        name=f'[{user["first_name"]} {user["last_name"]}] {meeting["topic"]}',
        begin=datetime.strptime(meeting['start_time'], '%Y-%m-%dT%H:%M:%S%z'),
        duration=timedelta(minutes=meeting.get('duration', 90)),
      )
      ics_calendar.events.add(e)

  tmpdir = tempfile.mkdtemp(prefix='zoom-to-ics')
  local_output_path = os.path.join(tmpdir, 'zoom-calendar.ics')
  with open(local_output_path, 'w') as f:
    f.write(str(ics_calendar))

  session = boto3.session.Session()
  s3_client = session.client(
    's3',
    region_name=s3_region_name,
    endpoint_url=s3_endpoint_url,
    aws_access_key_id=s3_aws_access_key_id,
    aws_secret_access_key=s3_aws_secret_access_key,
  )
  s3_client.upload_file(
    local_output_path,
    s3_bucket,
    s3_output_path,
    ExtraArgs={'ACL': 'public-read'},
  )
  print('Complete')



def main():
  from dotenv import load_dotenv
  load_dotenv()
  run(
    zoom_api_key=os.getenv('ZOOM_API_KEY'),
    zoom_api_secret=os.getenv('ZOOM_API_SECRET'),
    timezone=os.getenv('TIMEZONE'),
    s3_region_name=os.getenv('S3_REGION_NAME'),
    s3_endpoint_url=os.getenv('S3_ENDPOINT_URL'),
    s3_aws_access_key_id=os.getenv('S3_AWS_ACCESS_KEY_ID'),
    s3_aws_secret_access_key=os.getenv('S3_AWS_SECRET_ACCESS_KEY'),
    s3_bucket=os.getenv('S3_BUCKET'),
    s3_output_path=os.getenv('S3_OUTPUT_PATH'),
  )

if __name__ == '__main__':
  main()
