import cv2
import os
import fitz
import random
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


def pdfSeparator(ipDIR, opDIR1, opDIR2, pdf, params):

    if not pdf:
        return
    for pd in pdf:
        print("pdf  --> {}".format(pd))
        doc = fitz.open(os.path.join(ipDIR,pd))
        pgCount = len(doc)
        if pgCount<10:
            randm = list(range(pgCount))
        else:
            randm = random.sample(range(pgCount),10)

        prob = []
        for pageN in randm:
            page = doc.loadPage(pageN) #number of page
            pix = page.getPixmap()
            pix.writePNG("outfile.png")
            rawImg = cv2.imread("outfile.png")
            prob.append(predict(rawImg,params))
            os.remove("outfile.png")
            
        doc.close()
        if prob.count(1)>len(prob)*0.8:
            os.rename(os.path.join(ipDIR, pd),os.path.join(opDIR1, pd))
        else:
            os.rename(os.path.join(ipDIR, pd),os.path.join(opDIR2, pd))

