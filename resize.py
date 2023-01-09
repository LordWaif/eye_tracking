import cv2
import numpy as np
from pathlib import Path

bg_paths = Path('/home/lordwaif/documents/usecase_andiara/imgs').glob('*')
for path in bg_paths:
    ...
    image = cv2.imread(path.__str__())
    image_resized = cv2.resize(image, (1920,1080),  
               interpolation = cv2.INTER_NEAREST) 
    cv2.imwrite(path.__str__(),image_resized)
#print(bg_paths)