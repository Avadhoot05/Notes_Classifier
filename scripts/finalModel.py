import numpy as np
import os
import multiprocessing
from InputData import prepareInput
from ImageHandlling import imageSeparator
from videoHandlling import videoSeparator 
from pdfHandlling import pdfSeparator

def load_params(path_to_model, printParamsShape=False):
    model =np.load(path_to_model,allow_pickle=True)
    params = {"W1":model[()]['W1'],
              "W2":model[()]['W2'],
              "W3":model[()]['W3'],
              "b1":model[()]['b1'],
              "b2":model[()]['b2'],
              "b3":model[()]['b3']}
    
    if printParamsShape:
        print("W1-->",params["W1"].shape)
        print("b1-->",params["b1"].shape)
        print("W2-->",params["W2"].shape)
        print("b1-->",params["b2"].shape)
        print("W3-->",params["W3"].shape)
        print("b3-->",params["b3"].shape)
    return params


if __name__=="__main__":
    path_to_model = "C:/Users/khede/OneDrive/Desktop/DESKTOP/Notes Classifier/trained_params.npy"
    ipDIR = "C:/Users/khede/OneDrive/Desktop/DESKTOP/test"
    opDIR1 = "C:/Users/khede/OneDrive/Desktop/DESKTOP/NotesFolder" 
    opDIR2 ="C:/Users/khede/OneDrive/Desktop/DESKTOP/NonNotesFolder"
    pd = int(input("Select PDF??Enter 1 else 0"))
    vd = int(input("Select Videos??Enter 1 else 0"))

    params = load_params(path_to_model=path_to_model)
    print("Trained Parameters Loaded Sucessfully!!!!\n")

    data = prepareInput(ipDIR=ipDIR, opDIR1= opDIR1, opDIR2=opDIR2, pd=pd, vd=vd)
    print("data preparation done!!")


    if pd and vd:
        p1 = multiprocessing.Process(target=imageSeparator, args=(ipDIR,opDIR1,opDIR2,data[0],params))
        p2 = multiprocessing.Process(target=videoSeparator, args=(ipDIR,opDIR1,opDIR2,data[1],params))
        p3 = multiprocessing.Process(target=pdfSeparator, args=(ipDIR,opDIR1,opDIR2,data[2],params))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()        

    else:

        if not pd and not vd:
            p1 = multiprocessing.Process(target=imageSeparator, args=(ipDIR,opDIR1,opDIR2,data[0],params))
            p2 = multiprocessing.Process(target=imageSeparator, args=(ipDIR,opDIR1,opDIR2,data[1],params))


        elif pd and not vd:
            p1 = multiprocessing.Process(target=imageSeparator, args=(ipDIR,opDIR1,opDIR2,data[0],params))
            p2 = multiprocessing.Process(target=pdfSeparator, args=(ipDIR,opDIR1,opDIR2,data[1],params))


        elif not pd and vd:
            p1 = multiprocessing.Process(target=imageSeparator, args=(ipDIR,opDIR1,opDIR2,data[0],params))
            p2 = multiprocessing.Process(target=videoSeparator, args=(ipDIR,opDIR1,opDIR2,data[1],params))

        p1.start()
        p2.start()

        p1.join()
        p2.join()
    