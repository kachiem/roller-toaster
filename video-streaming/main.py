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
from flask import Flask, render_template, Response, request
from flask import jsonify
from camera import VideoCamera
from google.cloud import videointelligence
import os
import io
import collections
import Tkinter
from threading import Thread

from google.cloud import vision
from google.cloud.vision import types




app = Flask(__name__)

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
client = vision.ImageAnnotatorClient()
#word = "pppppp"
global label_output
label_output = ""

@app.route('/')
def index():
    
    return render_template("index.html", top="random string to try")
    




def getTop(word):
    print word,'hi'
    top=word
    return render_template("index.html",top=top)
    #return word

"""@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)"""
        
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
    
label_output = ''
def gen(camera):
    
    """while True:
        frame = camera.get_frame()
        Thread(target = show(camera)).start()
        Thread(target = see(camera)).start()"""
    stuff = []
    bruh = 1
    while True:
        bruh-=1
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #print("hi")
        
        #input_content = frame.read()
        
        image = types.Image(content=frame)
        
        if bruh == 0:
            bruh=10
            response = client.label_detection(image=image)
            labels = response.label_annotations
            """if len(labels) > 0:
                word = labels[0].description
                top = word
                print word
                label_output = word"""
                #the_top(label_output)
                #getTop(word)
                
                #@app.route("/theTop", methods=['POST'])
                #theTop(word)
            #print('Labels:')
            annotations = {}
            for label in labels:
                annotations[label.score] = label.description
                # annotations = dict(zip(confidences, labels))
            sorted_anno = collections.OrderedDict(sorted(annotations.items(), reverse=True))
            #print "\n\n\n "
            os.system('clear')
            thisArray = []
            d = {}
            for confs, lbls in sorted_anno.items():
                lab = str(lbls)
                tab = "\t\t"
                if len(lab) > 7:
                    tab ="\t"

                
                outstr = str(lbls) + tab + "{0:.2f}".format(confs)
                d[lab] = outstr
                
                thisArray.append(lab)
            oldStuff = [""]*10       
            print "Item\t\tConfidence\n--------------------------"
            indices = range(0,10)
            for i in range (0,len(stuff)):
                if stuff[i] in thisArray:
                    oldStuff[i] = stuff[i]
                    indices.remove(i)
                #else:
                    #indices.append(i)
            #print oldStuff, thisArray,indices
            for item in thisArray:
                if item not in oldStuff:
                    oldStuff[indices.pop(0)] = item
            for item in oldStuff:
                if item != '':
                    print d[item]
            stuff = oldStuff
                    
                
            #print outstr
            #print(confs, lbls)
                

                
        
        

        
@app.route("/", methods=['GET','POST'])
def the_top(label_output):
    print label_output
    #top = word
    #print top,word,'asdfasdf'
    #return jsonify(top=top)
    #return top
    #return Response(word)
    #top = word#word = getTop()
    #print top,word
    with app.app_context():
        return render_template("index.html", top=label_output)

@app.route('/video_feed')
def video_feed():

    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)