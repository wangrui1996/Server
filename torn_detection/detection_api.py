import cv2
import torn_detection.Detect as Detect
detect_model_path = "./torn_detection/models/detect.tflite"
classifier_model_path = "./torn_detection/models/classifier.tflite"
#image_path = "demo.jpg"
#image = cv2.imread(image_path)
#input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
detect = Detect.Detect(detect_model_path, classifier_model_path)
def detect_image(image, score=0.5):
    detect.detect(image)
    return detect.draw_image(image, score)

#detect = Detect.Detect(model_path)
#cap = cv2.VideoCapture(0)
#ret, image = cap.read()
#while ret:
#    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#    detect.detect(image)
#    _, image = detect.draw_image(image)
#    cv2.imshow("demo", image)
#    cv2.waitKey(1)
#    ret, image = cap.read()