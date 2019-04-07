import numpy as np
import collections
from timeit import default_timer as timer
from google.cloud import videointelligence

start = timer()

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
operation = video_client.annotate_video(
    'gs://demomaker/cat.mp4', features=features)
print('\nProcessing video for label annotations...')

result = operation.result(timeout=120)
print('\nFinished processing.')

# write labels and confidences to .txt file
labels = []
confidences = []

segment_labels = result.annotation_results[0].segment_label_annotations
for i, segment_label in enumerate(segment_labels):
    lbl = '{}'.format(segment_label.entity.description) + ' '
    labels.append(lbl)

    for i, segment in enumerate(segment_label.segments):
        start_time = (segment.segment.start_time_offset.seconds +
                      segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        confidence = segment.confidence
        confs = '{}'.format(confidence) + '\n'
        confidences.append(confs)

annotations = dict(zip(confidences, labels))

# order results by confidence.
sorted_anno = collections.OrderedDict(sorted(annotations.items(), reverse=True))

# print results to table on gui.
for confs, lbls in sorted_anno.items():
    print(confs, lbls)
  

end = timer()
print('\n',end - start, 'sec')