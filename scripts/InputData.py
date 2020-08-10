import filetype
import os
import numpy as np

def splitFormat(ipDIR, images):
    image, videos, pdf = [],[],[]
    for i in images:
        kind = filetype.guess(os.path.join(ipDIR,i))
        
        if kind:
            if kind.mime.split('/')[0] == 'image':
                image.append(i)
            elif kind.mime.split('/')[0] == 'video':
                videos.append(i)
            else:
                pdf.append(i)
            
    return (image, videos, pdf)           



def prepareInput(ipDIR,opDIR1,opDIR2,pd,vd):
    for dir in (opDIR1,opDIR2):        
        try:
            os.mkdir(dir)
        except FileExistsError:
            print("{} folder already exist.\npress 1 to continue\npress 0 to exit".format(dir.split("/")[-1]))
            x = int(input())
            if x:
                pass
            else:
                exit()



    X_imgList = os.listdir(ipDIR) 
    

    data = splitFormat(ipDIR,X_imgList) 
    
    if not pd and not vd:
        le = len(data[0])
        first_half = data[0][:le//2]
        second_half = data[0][le//2:]
        return (first_half,second_half)

    if pd and not vd:
        return (data[0],data[2])
    
    if not pd and vd:
        return (data[0],data[1])    
    return data 







    
