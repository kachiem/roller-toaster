import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #url = "http://100.82.255.163:4747/mjpegfeed?640x480"
        # self.video = cv2.VideoCapture(0)
        #self.video = cv2.VideoCapture('http://100.82.250.3:4747/mjpegfeed?640x480')
        self.video = cv2.VideoCapture('http://100.82.133.200:4747/mjpegfeed?640x480')
        #self.video = cv2.VideoCapture('gs://demomaker/cat.mp4')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
         #self.video = cv2.VideoCapture('arnolddies.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()