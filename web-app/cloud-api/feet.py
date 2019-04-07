import numpy as np
import collections
from timeit import default_timer as timer
from google.cloud import videointelligence

start = timer()

"""Object Tracking."""
from google.cloud import videointelligence_v1p2beta1 as videointelligence

# It is recommended to use location_id as 'us-east1' for the best latency
# due to different types of processors used in this region and others.
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.OBJECT_TRACKING]
operation = video_client.annotate_video(
    input_uri=gcs_uri, features=features, location_id='us-east1')
print('\nProcessing video for object annotations.')

result = operation.result(timeout=300)
print('\nFinished processing.\n')

# The first result is retrieved because a single video was processed.
object_annotations = result.annotation_results[0].object_annotations

# Find feet!
object_annotation = object_annotations[0]
print('Entity description: {}'.format(
    object_annotation.entity.description))
if object_annotation.entity.entity_id:
    print('Entity id: {}'.format(object_annotation.entity.entity_id))

print('Segment: {}s to {}s'.format(
    object_annotation.segment.start_time_offset.seconds +
    object_annotation.segment.start_time_offset.nanos / 1e9,
    object_annotation.segment.end_time_offset.seconds +
    object_annotation.segment.end_time_offset.nanos / 1e9))

print('Confidence: {}'.format(object_annotation.confidence))

# Here we print only the bounding box of the first frame in this segment
frame = object_annotation.frames[0]
box = frame.normalized_bounding_box
print('Time offset of the first frame: {}s'.format(
    frame.time_offset.seconds + frame.time_offset.nanos / 1e9))
print('Bounding box position:')
print('\tleft  : {}'.format(box.left))
print('\ttop   : {}'.format(box.top))
print('\tright : {}'.format(box.right))
print('\tbottom: {}'.format(box.bottom))
print('\n')


end = timer()
elapsed = end - start