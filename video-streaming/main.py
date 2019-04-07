#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
from camera import VideoCamera
from google.cloud import videointelligence
import os
import io
from threading import Thread

from google.cloud import vision
from google.cloud.vision import types


app = Flask(__name__)

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
client = vision.ImageAnnotatorClient()
word = ""

@app.route('/')
def index():
    return render_template('index.html', top=word)
    

#@app.route("/user/")

def see(frame):

    #frame = camera.get_frame()
    #yield (b'--frame\r\n'
           #b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    #print("hi")

    #input_content = frame.read()

    operation = video_client.annotate_video(
            features=features, input_content=frame)
    print("hi2")
    result = operation.result(timeout=60)
    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')
        
def show(frame):

    #frame = camera.get_frame()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
def gen(camera):
    """while True:
        frame = camera.get_frame()
        Thread(target = show(camera)).start()
        Thread(target = see(camera)).start()"""
    i = 0
    while True:
        i+=1
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #print("hi")
        
        #input_content = frame.read()
        
        image = types.Image(content=frame)
        
        if i == 20:
            i=0
            response = client.label_detection(image=image)
            labels = response.label_annotations
            if len(labels) > 0:
                word = labels[0].description
                top = word
                print word
            #print('Labels:')
            #for label in labels:
                #print(label.description,label.score)
                
                
        
        
        """operation = video_client.annotate_video(
                features=features, input_content=frame)
        print("hi2")
        result = operation.result(timeout=60)
        print('\nFinished processing.')

        # first result is retrieved because a single video was processed
        segment_labels = result.annotation_results[0].segment_label_annotations
        for i, segment_label in enumerate(segment_labels):
            print('Video label description: {}'.format(
                segment_label.entity.description))
            for category_entity in segment_label.category_entities:
                print('\tLabel category description: {}'.format(
                    category_entity.description))

            for i, segment in enumerate(segment_label.segments):
                start_time = (segment.segment.start_time_offset.seconds +
                              segment.segment.start_time_offset.nanos / 1e9)
                end_time = (segment.segment.end_time_offset.seconds +
                            segment.segment.end_time_offset.nanos / 1e9)
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = segment.confidence
                print('\tSegment {}: {}'.format(i, positions))
                print('\tConfidence: {}'.format(confidence))
            print('\n')"""
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)