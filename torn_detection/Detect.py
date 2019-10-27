import cv2
import numpy as np
import tensorflow as tf

class Detect:
    def __init__(self, model_path):
        # Load TFLite model and allocate tensors.
        self.interpreter = tf.lite.Interpreter(model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
        input_dtype = self.input_details[0]['dtype']
        self.input_data = np.array(np.random.random_sample(self.input_shape), dtype=input_dtype)

    def detect(self, image):
        if image.shape[0] != self.input_shape[1] or image.shape[1] != self.input_shape[2]:
            image = cv2.resize(image, (self.input_shape[2], self.input_shape[1]))
        self.input_data[0, :, :, :] = image
        self.input_data = self.input_data - 127
        self.input_data = self.input_data / 127
        self.interpreter.set_tensor(self.input_details[0]['index'], self.input_data)
        self.interpreter.invoke()
        self.targets_positions = self.interpreter.get_tensor(self.output_details[0]['index'])
        self.targets_label = self.interpreter.get_tensor(self.output_details[1]['index'])
        self.targets_score = self.interpreter.get_tensor(self.output_details[2]['index'])
        self.targets_number = self.interpreter.get_tensor(self.output_details[3]['index'])

    def draw_image(self, image, score=0.5):
        img_h, img_w,_ = image.shape
        have_target = False
        for idx in range(int(self.targets_number)):
            if self.targets_score[0][idx] <= score:
                break
            def get_Absolute_coordinates(Relative_coordinates, image_height, image_width):
                return int(Relative_coordinates[1] * image_width), \
                int(Relative_coordinates[0] * image_height), \
                int(Relative_coordinates[3] * image_width), \
                int(Relative_coordinates[2] * image_height)
            have_target = True
            xmin, ymin, xmax, ymax = get_Absolute_coordinates(self.targets_positions[0][idx], img_h, img_w)
            image = cv2.rectangle(image, (xmin, ymin), (xmax , ymax), (0, 0, 255), int(min(img_h,img_w) / 100))
#            print(self.targets_label[0][idx])
        return have_target, image



