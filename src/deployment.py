#! /usr/bin/env python
# -*- coding: utf-8 -*-
from io import BytesIO
import base64
from src.algorithm.ppgan.apps import Photo2CartoonPredictor
import os


p2c = Photo2CartoonPredictor()

def apply(method, input_data): 

    if method == 'photo2cartoon':
        imgdata = input_data.get('imgdata', None)
        byte_data = base64.b64decode(imgdata)
        image_data = BytesIO(byte_data)
        output_buffer = p2c.run(image_data)
        byte_data = output_buffer.getvalue()
        return byte_data
    elif method == 'face_parser':
        return 
    elif method == 'makeup':
        return
    elif method == 'pixel2pixel':
        return
    elif method == 'motion_driving':
        return
    elif method == 'wav2lip':
        return
