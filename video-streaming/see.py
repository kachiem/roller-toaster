from google.cloud import videointelligence
import os
import io
import cv2

#GOOGLE_APPLICATION_CREDENTIALS = "Users/michellecaplin/Downloads/video_streaming_with_flask_example-master/roller toaster-69692fb29fba.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./roller toaster-69692fb29fba.json"
print("hi")
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
#operation = video_client.annotate_video(
    #'gs://demomaker/cat.mp4', features=features)
#with io.open("./arnolddies.mp4", 'rb') as movie:
    #input_content = movie.read()
#video = cv2.VideoCapture(0)

operation = video_client.annotate_video(
        features=features, input_content=input_content)
#operation = video_client.annotate_video(
#'file:///arnolddies.mp4', features=features)
print('\nProcessing video for label annotations:')

result = operation.result(timeout=120)
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