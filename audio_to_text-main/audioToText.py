from __future__ import print_function
from flask import *
import json
import time
import boto3
import json
import requests
from pydub import AudioSegment
import urllib.request
from os import path
import subprocess
import os


app = Flask(__name__)
aws_access_key_id = "aws_access_key_id_here"
aws_secret_access_key = "aws_secret_access_key_here"
aws_region = "aws_region_here"
aws_bucket="aws_bucket_here"
aws_folder="aws_folder_here"
vocabulary_name="vocabulary_name"

transcribe = boto3.client('transcribe',
                          aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

@app.route('/speech',methods = ['POST'])
def speech():
    if request.method=='POST':
        # print("___________*************************************__________")
        data=json.loads(request.data)
        url=data['audioUrl']
        audioType=data['audioType']
        file_name=str(url.split('/')[-1:][0])
        audioFormat = 'mp3'
        if audioType=='recorded':
          print('Downloading file......')
          urllib.request.urlretrieve(url, 'sample.mp3')
          AudioSegment.from_file("sample.mp3").export("test.mp3", format="mp3")
          os.remove("sample.mp3")
          uploaded = upload_to_aws('test.mp3', aws_bucket,"uat-audios/"+file_name )
          os.remove('test.mp3')
        else:
          audioFormat = 'mp4'

        #file_name=str(url.split('/')[-1:][0])
        job_uri="s3://{aws_bucket}/{aws_folder}/{file_name}".format(aws_bucket=aws_bucket,aws_folder=aws_folder,file_name=file_name)
        try:
            transcribe.start_transcription_job(
                        TranscriptionJobName=file_name,
                        Media={'MediaFileUri': job_uri},
                        MediaFormat=audioFormat,
                        LanguageCode='en-IN',
                        Settings={
                             "VocabularyName": vocabulary_name,
                             # 'ShowSpeakerLabels': True,
                             # 'MaxSpeakerLabels':2
                        },
                        )
            
        except Exception as e:
          try:
            status = transcribe.get_transcription_job(TranscriptionJobName=file_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED']:
              request1 = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
              response = request1.text
              response = json.loads(response)
              res=response['results']['transcripts'][0]['transcript']
              print(res)
              return jsonify(res);
                
          except Exception as e:
            return jsonify("error")
        

        try:
          while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=file_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
          print("done")
          request1 = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
          response = request1.text
          response = json.loads(response)
          res=response['results']['transcripts'][0]['transcript']
          print(res)
          return jsonify(res)

        except Exception as e:
          return jsonify("error")
          


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False






# if __name__ == '__main__':
#    app.run(debug = True)

app.run(host='0.0.0.0', port='4992')

