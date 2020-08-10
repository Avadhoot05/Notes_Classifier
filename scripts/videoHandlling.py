import cv2
import os
import numpy as np


def relu(Z):
    return np.maximum(Z,0)

def predict(img,params):
    cvt = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    rimg = cv2.resize(cvt,(64,64))
    img_np_arr = np.array(rimg,dtype="float32")
    img_flat = img_np_arr.reshape(12288,1)
    img_norm = img_flat/255

    assert img_norm.shape == (12288,1)

    Z1 = np.dot(params["W1"],img_norm)+params["b1"]
    A1 = relu(Z1)

    Z2 = np.dot(params["W2"],A1)+params["b2"]
    A2 = relu(Z2)

    Z3 = np.dot(params["W3"],A2)+params["b3"]

    predVal= np.squeeze(Z3)
    return predVal[0]<predVal[1]


        
def videoSeparator(ipDIR, opDIR1, opDIR2, videos, params):
	if not videos:
		return
	for vid in videos:
		print("video--> {}".format(vid))
		prob=[]
		cap = cv2.VideoCapture(os.path.join(ipDIR, vid))
		ret,frame = cap.read()
		ct=0
		
		while ret and ct<1000:
			if not ct % 60:
				prob.append(predict(frame,params))

			ret,frame= cap.read()
			ct+=1

		cap.release()
		if prob.count(1)>len(prob)*0.7:
			os.rename(os.path.join(ipDIR, vid),os.path.join(opDIR1, vid))
		else:
			os.rename(os.path.join(ipDIR, vid),os.path.join(opDIR2, vid))





