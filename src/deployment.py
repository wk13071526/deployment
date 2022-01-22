#! /usr/bin/env python
# -*- coding: utf-8 -*-
from io import BytesIO
import base64
from src.algorithm.ppgan.apps import Photo2CartoonPredictor
import os


def apply(input_data):
    imgdata = input_data.get('imgdata', None)
    byte_data = base64.b64decode(imgdata)
    image_data = BytesIO(byte_data)
    p2c = Photo2CartoonPredictor() 
    p2c.run(image_data)
    with open('/home/deployment/output/p2c_cartoon.png', 'rb') as f:
        img = f.read()
    os.remove('/home/deployment/output/p2c_cartoon.png')
    #image_bytes = data.tobytes()
    image_base64 = base64.b64encode(img)
    return image_base64
