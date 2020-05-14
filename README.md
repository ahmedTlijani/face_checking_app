### Face checking api using [@Face recognition library](https://github.com/ageitgey/face_recognition).

### Development  
- Install [@Face recognition library](https://github.com/ageitgey/face_recognition).
- Install flask

### Run  
```python
set FLASK_APP= python-api-verification.py
set FLASK_ENV= development
flask run
```

> Running on http://127.0.0.1:5000/

### How to use
``Send post request  to @python-api-url (http://127.0.0.1:5000/api/verify face/) ``

- Sent data form 

``data = { cin : "", known_image : "", unknown_image:"" } ``

- cin:  id
- known_image, unknown_image: the images to compare

- Received data form 

``
data = { 'status'  : '','message' :'' }
``

>status can be : 

```
        data["status"] = 'OK'
        data["message"] = ("The two faces are equal")
		
        data["status"] = 'FAIL'
        data["message"] = ("The two faces are different")

        data["status"] = 0
        data["message"] = ("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
```

