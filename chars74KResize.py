#A simple program to resize the Chars74K dataset to 40x40 images and invert the colours
import os,cv2, numpy as np 
from PIL import Image, ImageOps, ImageFilter
from tqdm import tqdm
os.chdir(os.path.dirname(os.path.realpath(__file__)))
masterdir=os.listdir("Chars74KResized/")
for i in range(len(masterdir)):
    subdir=os.listdir("Chars74KResized/"+masterdir[i])
    for j in tqdm(range(len(subdir)),ascii=True, desc=masterdir[i]+": "):
        try:
            im=Image.open("Chars74KResized/"+masterdir[i]+"/"+subdir[j])
            im=im.resize((30,30),Image.ANTIALIAS) #Resizes the image
            im=np.array(im)
            _,thresholded=cv2.threshold(im,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            im=Image.fromarray(thresholded)
            im=im.filter(ImageFilter.SMOOTH_MORE)
            im.save("charImages/train/"+masterdir[i]+"_ch"+str(j)+".png")#Saves the image
        except:
            pass
