from keras.models import load_model,Model
import cv2
import numpy as np
import numpy as np
from keras.preprocessing import image

bubble_m = load_model("/home/vasu/all_projects/SIH/VisualTireInspectorBackend/dummy/ML_models/bubble.h5")
bladder_m = load_model("/home/vasu/all_projects/SIH/VisualTireInspectorBackend/dummy/ML_models/cease.h5")
scorch_m = load_model("/home/vasu/all_projects/SIH/VisualTireInspectorBackend/dummy/ML_models/soched.h5")


def nn_models(img):
	img_ = image.load_img(img,target_size=(100,100))
	img_array = image.img_to_array(img_)
	img_in = img_array.reshape((1, 100 ,100, 3))

	bubble1 = bubble_m.predict_classes(img_in)[0]
	bladder1 = bladder_m.predict_classes(img_in)[0]
	scorch1 = scorch_m.predict_classes(img_in)[0]
	return [bubble1,bladder1,scorch1]


def circle_p(img):

    im = cv2.imread(img)
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ou = im.copy()
    
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2, minDist=160)
 
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        z = circles.shape[0]
        print z
        if z == 1:
            return 1
        return 0

def ink_spot(img):

    img = cv2.imread(img)
    lower = np.asarray([33, 11, 100]).astype('uint8')
    upper = np.asarray([88, 89, 200]).astype('uint8')
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask = mask)
    score =  output.sum()/(img.shape[1]*img.shape[0])
    if score >= 0.25:
        return 1
    return 0

def predict_defect(img):

	out_list = nn_models(img)
	out_list.append(circle_p(img))
	out_list.append(ink_spot(img))
	print (out_list)
	return out_list



