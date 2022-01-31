#! /usr/bin/env python
# -*- coding: utf-8 -*-
from io import BytesIO
import base64
from src.algorithm.ppgan.apps import Photo2CartoonPredictor
import os


p2c = Photo2CartoonPredictor()

def apply(input_data):
    

    imgdata = input_data.get('imgdata', None)
    byte_data = base64.b64decode(imgdata)
    image_data = BytesIO(byte_data)
    output_buffer = p2c.run(image_data)
    byte_data = output_buffer.getvalue()
    image_base64 = base64.b64encode(byte_data)
    
    return image_base64
