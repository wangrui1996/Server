from flask import Flask, render_template, Response, redirect, request, url_for, send_from_directory, make_response, jsonify
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from torn_detection.detection_api import detect_image
UPLOAD_FOLDER = "./"
ALLOWED_EXTENSIONS = set(['jpg', 'mp4', 'zip'])

frequency = cv2.getTickFrequency()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 50 # 16 * 50 MB

fontpath = "./app/static/demo.ttc" # <== 这里是宋体路径

b,g,r,a = 0,0,255,0
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
import numpy

@app.route('/torn', methods=['GET', 'POST'])
def tornDetection():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filestr = file.read()
            # convert string data to numpy array
            npimg = numpy.fromstring(filestr, numpy.uint8)
            # convert numpy array to image
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            def progress(image):
                ret, image = detect_image(image)
                h,w,_ = image.shape
                import cv2
                img_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(img_pil)
                size = int(min(h,w) / 10)
                print("3: " ,size)
                font = ImageFont.truetype(fontpath, size)
                if ret:
                    text_str = "包裹破损"
                else:
                    text_str = "没有破损"
                draw.text((int(w/8), int(h/4)), text_str, font=font, fill=(b,g,r,a))
                image = np.array(img_pil)

                #image = cv2.putText(image, "{} Torn".format(ret), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 255, 0), 5)
                return image

            img = progress(img)

            img_encode = cv2.imencode('.jpg', img)[1]
            # imgg = cv2.imencode('.png', img)

            data_encode = np.array(img_encode)

            response = make_response(data_encode.tostring())
            response.headers['Content-Type'] = 'image/png'
            return response
    #        return redirect(url_for('face_upload_img',filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload>
        </form>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=False, threaded=True)
