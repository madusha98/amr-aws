import numpy as np
import cv2
import os
from flask import Flask, request, Response, jsonify
import jsonpickle
import base64
import json
from flask import jsonify
from requests_toolbelt import MultipartDecoder
from PIL import Image
import io

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.1

def get_predection(image):
    net = cv2.dnn.readNet("./yolo-model/yolov4-tiny-obj.cfg", "./yolo-model/yolov4-tiny-obj_best.weights")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

    with open('./yolo-model/labels.txt', 'rt') as f:
        names = f.read().rstrip('\n').split('\n')

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255)

    classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    print(classes)
    res = []
    for i in range(len(classes)):
        res.append({"class": classes[i][0], "x": boxes[i][0], "score": scores[i][0]})

    res = sorted(res, key=lambda k: k['x']) 
    return res

def validate_predection(data):
    if (len(data) != 5):
        return {'error': 'Something went wrong. Please try again'}
    
    value = [item['class'] for item in data]
    value = ''.join(map(str,value))

    avgScore = np.mean([item['score'] for item in data])

    return  {'value': value, 'score': float(avgScore)}


def get_reading(event):

    body = event["body"]
    content_type = ""
    try:
        content_type = event["headers"]["Content-Type"]
    except:
        content_type = event["headers"]["content-type"]
        
    body_dec = base64.b64decode(body)
    multipart_data = MultipartDecoder(body_dec, content_type)

    binary_content = []
    for part in multipart_data.parts:
        binary_content.append(part.content)

    imageStream = io.BytesIO(binary_content[0])
    img = Image.open(imageStream)
    # npimg=np.array(img)
    # img = request.files["image"]
    # npimg = np.fromfile(img, np.uint8)
    # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    predection = get_predection(img)
    res = validate_predection(predection)
    return res




    # binary_content = []
    # for part in multipart_data.parts:
    #     binary_content.append(part.content)

    # imageStream = io.BytesIO(binary_content[0])
    # img = Image.open(imageStream)
    # npimg=np.array(img)
    # image=npimg.copy()
    # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # res=get_predection(image,nets,Lables,Colors)
    # # image=cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
    # # np_img=Image.fromarray(image)
    # # img_encoded=image_to_byte_array(np_img)
    # # return Response(response=img_encoded, status=200,mimetype="image/jpeg")
        
    # res = sorted(res, key=lambda k: k['x']) 
    # res = [item['class'] for item in res]
    # res = ''.join(map(str,res))
    # return res
