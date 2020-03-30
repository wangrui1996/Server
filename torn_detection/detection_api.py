import cv2
import os
#import torn_detection.Detect as Detect
#detect_model_path = "./torn_detection/models/detect.tflite"
#classifier_model_path = "./torn_detection/models/classifier.tflite"
#image_path = "demo.jpg"
#image = cv2.imread(image_path)
#input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#detect = Detect.Detect(detect_model_path, classifier_model_path)
#def detect_image(image, score=0.5):
#    detect.detect(image)
#    return detect.draw_image(image, score)

package_detect_path = os.path.join(os.path.dirname(__file__),"models", "package.tflite")
torn_detect_path =  os.path.join(os.path.dirname(__file__),"models", "torn.tflite")

from torn_detection.tfLite import Detect
package_detect = Detect(package_detect_path)
torn_detect = Detect(torn_detect_path)
def detect_imagev2(image, package_score=0.5, torn_score=0.5):
    package_detect.detect(image, package_score)
    image_show = image.copy()
    image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    have_target, image_show = package_detect.draw_image(image_show)
    if not have_target:
        return have_target, image_show
    image_h, image_w, _ = image.shape
    have_torn = False
    for rect in package_detect.get_detection_rect():
        xmin, ymin, xmax, ymax = package_detect.conver_to_abs_axis(rect, image_h, image_w)
        package_roi = image[ymin:ymax, xmin:xmax, :]
        # cv2.imshow("package_roi", package_roi)
        torn_detect.detect(package_roi, torn_score)
        #have_torn, pacakge_roi = torn_detect.draw_image(package_roi)
        # cv2.imshow("pacakge", pacakge_roi)
        have_torn, image_show[ymin:ymax, xmin:xmax, :] = torn_detect.draw_image(image_show[ymin:ymax, xmin:xmax, :], True)
    return have_torn, image_show



