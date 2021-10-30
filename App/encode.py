import json
from json import JSONEncoder
import cv2
import numpy as np
import face_recognition
from PIL import Image,ExifTags
from pathlib import Path

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def imagencode(name,filepath):
    
    #print(type(filepath))
    image = cv2.imread(filepath)
    #image=Image.open(filepath)

    try :
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(image._getexif().items())

        if   exif[orientation] == 3 : 
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            image=image.rotate(90, expand=True)

    except : 
        pass
            
        
    #image = face_recognition.load_image_file(image)
    encode=face_recognition.face_encodings(image)[0]
    print('done encoding')
    


    numpyArrayOne = encode

    # Serialization
    encodedNumpyData = json.dumps(numpyArrayOne, cls=NumpyArrayEncoder)  # use dump() to write array into file
    numpyData = {'name':name,
    'face': encodedNumpyData
    }
    print("json done")
    return  numpyData

def imgdecode(facestr):
    # Deserialization
    print("Decode JSON serialized NumPy array")
    decodedArrays=[]
    for cface in facestr:
        decodedArrays.append(json.loads(cface))

    finalNumpyArray = np.array(decodedArrays)
    print("NumPy Array done")
    return finalNumpyArray