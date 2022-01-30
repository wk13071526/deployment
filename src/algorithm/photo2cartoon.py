import sys
from src.algorithm.ppgan.apps import Photo2CartoonPredictor
#sys.path.append("./")

p2c = Photo2CartoonPredictor(output_path='output')
p2c.run('test_img.jpg')
