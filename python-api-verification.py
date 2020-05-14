#goign to use flask to make the api http://flask.pocoo.org/
###

import face_recognition
from flask import Flask  
from flask import request, Response
# flask cors - allow cross origin https://flask-cors.readthedocs.io/en/latest/
from flask_cors import CORS, cross_origin
import json
import urllib.request
# base64 to image
from PIL import Image
import base64
from io import BytesIO
import os # get director path
import time


app = Flask(__name__)
#deploy service


# Image iformation
temp_path = 'temporary_images_/'
image_type = 'jpg'
# handle responses
data = {
        'status'  : '',
        'message' :''
    }

#http://127.0.0.1:5000/api/verify-face/
@app.route("/api/verify-face/",methods=["POST"])
@cross_origin()
def get_base64_images():
    dataObject = request.get_json() # get post data
    #print(dataObject["cin"])
    cin = dataObject["cin"]
    known_image_b64 = dataObject["known_image"]
    unknown_image_b64 = dataObject["unknown_image"]
    
    try:
        # save images 
        img1 = cin
        if save_temp_image(img1, known_image_b64): # save first image 
            img2 = cin + '_2'
            if save_temp_image(img2,unknown_image_b64): # save second image with _2 in the name
                #load images 
                img1_src = get_image_path(img1)
                img2_src = get_image_path(img2)
            else: return 0
        else: return 0
        
    except IndexError:
        return 0
        
    time.sleep(1) # wait 1 second then remove the image
    result = face_recognition_(img1_src,img2_src)
    if result=='OK':
        data["status"] = 'OK'
        data["message"] = ("The two faces are equal") # will return just OK of FAIL next
        
    elif result=='FAIL':
        data["status"] = 'FAIL'
        data["message"] = ("The two faces are different")
    else: # cant locate any faces -> retrun 0
        data["status"] = 0
        data["message"] = ("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


def save_temp_image(cin, base64image):
    try:
        #image creation from base64
        img = Image.open(BytesIO(base64.b64decode(base64image)))
        img_name = temp_path + str(cin) + '.' + image_type
        #print('-----------------------------------------------------')
        #print(img_name)
        img.save(img_name)
        return 1
    except IndexError:
        return 0

def get_image_path(cin):
    #print('---------------- Temporary Image Directory Path ---------------')
    temp_image_path = os.getcwd() + '/' + temp_path + cin + '.' + image_type
    #print(temp_image_path)
    return temp_image_path


def remove_img(image_path):
    os.remove(image_path)


# face_recognition function --> return true when the same face false if else
def face_recognition_(known_face_link_, unknown_face_link_):
    print('----------------------------------------')
    print(known_face_link_)
    print(unknown_face_link_)
    first_image = face_recognition.load_image_file(known_face_link_)
    unknown_image = face_recognition.load_image_file(unknown_face_link_)

    try:
        first_face_encoding = face_recognition.face_encodings(first_image)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0] 

    except IndexError:
        #print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        remove_img(known_face_link_)
        remove_img(unknown_face_link_)
        return(0)
        quit()

    known_face = [ first_face_encoding ]

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_face, unknown_face_encoding)
    
    print("----------------------------------------------------------------------")
    print('Are the two faces are equal? ')
    print(results[0])
    print("----------------------------------------------------------------------")
    if results[0]:
        remove_img(known_face_link_)
        remove_img(unknown_face_link_)
        print ("OK")
        return ("OK")
    else:
        remove_img(known_face_link_)
        remove_img(unknown_face_link_)
        print ("FAIL")
        return ("FAIL")


print ("_____python api with flask_____")

