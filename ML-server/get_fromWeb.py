import cv2
import urllib
import urllib.request as r
import numpy as np
import time

class ParseWeb():
    def __init__(self) -> None:
        self.url = 'http://192.168.1.22:8000/clean_feed'
        self.frame = np.zeros((480,480,3)).astype(np.uint8)
    
    def getImg(self):
        self.stream = r.urlopen(self.url)

        bytes = b''
        while True:
            bytes += self.stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                #cv2.imshow('i', self.frame)
                #if cv2.waitKey(1) == 27:
                #    exit(0)   

        
            