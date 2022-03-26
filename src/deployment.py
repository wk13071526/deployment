#! /usr/bin/env python
# -*- coding: utf-8 -*-
from io import BytesIO
import base64
from src.algorithm.ppgan.apps import Photo2CartoonPredictor
from src.algorithm.ppgan.apps import FaceParsePredictor
from easydict import EasyDict as edict
from src.algorithm.ppgan.utils.config import get_config
from src.algorithm.ppgan.apps import PSGANPredictor
import os


p2c = Photo2CartoonPredictor()
fp = FaceParsePredictor()

def apply(input_data): 
    method_type = input_data.get('type', None)
    if method_type == '1':
        imgdata = input_data.get('imgdata', None)
        byte_data = base64.b64decode(imgdata)
        image_data = BytesIO(byte_data)
        output_buffer = p2c.run(image_data)
        byte_data = output_buffer.getvalue()
        return byte_data
    elif method_type == '2':
        imgdata = input_data.get('imgdata', None)
        byte_data = base64.b64decode(imgdata)
        image_data = BytesIO(byte_data)
        output_buffer = fp.run(image_data)
        byte_data = output_buffer.getvalue()
        return byte_data 
    elif method_type == '3':
        params = dict()
        params["evaluate_only"] = True
        params["profiler_options"] = None
        params["seed"] = None
        params["config_file"] = "configs/makeup.yaml"
        params["model_path"] = "./params/psgan_weight.pdparams"
        params["source_path"] = "test_img.jpg"
        params["reference_dir"] = "reference_dir"
        return
    elif method_type == 'pixel2pixel':
        return
    elif method_type == 'motion_driving':
        return
    elif method_type == 'wav2lip':
        return
