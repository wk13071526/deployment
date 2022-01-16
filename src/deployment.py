#! /usr/bin/env python
# -*- coding: utf-8 -*-
from io import BytesIO
import base64


def apply(input_data):
    imgdata = input_data.get('imgdata', None)
    byte_data = base64.b64decode(imgdata)
    image_data = BytesIO(byte_data)
    # 推理代码
    ouput = "Success"
    return ouput
