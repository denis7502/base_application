import torch
import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
from scipy.spatial import distance
import numpy as np

class Detection():
    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5x', force_reload=True).to(self.device)
        self.model.classes = [41]
        self.model_2  = MTCNN(keep_all=True, device=self.device)
        self.drink = False
        self.cup = False

    def detect(self, frame):
        gray = self.model([frame])
        obj = np.array(gray.xyxy[0].cpu())
        boxes, pt = self.model_2.detect(frame)
        
        return obj, boxes

    def detectDrink(self, frame, obj, boxes):
        if not isinstance(boxes, type(None)):
            if len(boxes) > 0:
                boxes = boxes[0]
            if len(obj) > 0:
                if (obj[:, 5] == 41).any():
                    bx_cup = obj[obj[:, 5] == 41][0]
                    cup_min, cup_max = (int(bx_cup [0]), int(bx_cup[1])), (int(bx_cup[2]), int(bx_cup[3]))
                    frame = cv2.rectangle(frame, cup_min, cup_max,  (0, 255, 255), 5)
                    cup_x, cup_y = int((cup_min[0] + cup_max[0])/2), int((cup_min[1] + cup_max[1])/2)
                    frame = cv2.putText(frame, 'Cup', (cup_x, cup_y), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255, 0, 0), 2, cv2.LINE_AA)
                    self.cup = True
            else:
                self.cup = False
            if len(boxes) > 0:
                face_min, face_max = (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3]))
                face_x, face_y = int((face_min[0] + face_max[0])/2), int((face_min[1] + face_max[1])/2)
                frame = cv2.rectangle(frame, face_min, face_max, (255, 255, 255), 5)
                frame = cv2.putText(frame, 'Face', (face_x, face_y), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
            if self.cup:
                if distance.euclidean((face_x, face_y), (cup_x, cup_y)) <= abs(cup_min[1] - cup_max[1]):
                    frame = cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]),  (0, 255, 0), 5)
                    self.drink = True
                else:
                    self.drink = False
        else:
            frame = cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]),  (0, 0, 255), 10)
        
        return frame

    def run(self, frame):
        yolo_pred, facenet_pred = self.detect(frame)
        frame = self.detectDrink(frame, yolo_pred, facenet_pred)
        return frame