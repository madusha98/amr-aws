import numpy as np
import argparse
import time
import cv2
import os
from flask import Flask, request, Response, jsonify
import jsonpickle
import io as StringIO
import base64
from io import BytesIO
import io
import json
from PIL import Image
from flask import jsonify
import base64
from requests_toolbelt import MultipartDecoder


confthres=0.5
nmsthres=0.1

def get_labels(labels_path):
    lpath=labels_path
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS

def get_colors(LABELS):
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    return COLORS

def get_weights(weights_path):
    weightsPath = weights_path
    return weightsPath

def get_config(config_path):
    configPath = config_path
    return configPath

def load_model(configpath,weightspath):
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='PNG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def get_predection(image,net,LABELS,COLORS):
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    response = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                response.append({'class': int(classID), 'x': float(x)})
                

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            print(boxes)
            print(classIDs)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
    # return image
    return response



def get_reading(event):
  labelsPath='yolo-model/labels.txt'
  cfgpath='yolo-model/yolov2-tiny-obj.cfg'
  wpath='yolo-model/yolov2-tiny-obj_last.weights'
  Lables=get_labels(labelsPath)
  CFG=get_config(cfgpath)
  Weights=get_weights(wpath)
  nets=load_model(CFG,Weights)
  Colors=get_colors(Lables)

  # img = req.files["image"].read()
#   data = json.loads(event['body'])
#   name = data['name']
#   img = data['image']

  body = event["body"]
  content_type = event["headers"]["Content-Type"]
  body_dec = base64.b64decode(body)
  multipart_data = MultipartDecoder(body_dec, content_type)

  binary_content = []
  for part in multipart_data.parts:
    binary_content.append(part.content)

  imageStream = io.BytesIO(binary_content[0])
  img = Image.open(imageStream)
  npimg=np.array(img)
  image=npimg.copy()
  image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  res=get_predection(image,nets,Lables,Colors)
  # image=cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
  # np_img=Image.fromarray(image)
  # img_encoded=image_to_byte_array(np_img)
  # return Response(response=img_encoded, status=200,mimetype="image/jpeg")
    
  res = sorted(res, key=lambda k: k['x']) 
  res = [item['class'] for item in res]
  res = ''.join(map(str,res))
  return res
