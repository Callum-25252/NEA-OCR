from PIL import Image,ImageFont,ImageDraw,ImageFilter
import string,os,random,cv2,numpy as np
from tqdm import tqdm #Used for measuring progress
charlist=list(string.ascii_uppercase+string.digits)
#List all uppercase characters and all digits
os.chdir("charImages")
fontlist=(os.listdir("Fonts/")*8)
#List the fonts directory 8 times
for i in charlist:
    for j in tqdm(range(len(fontlist)+500),ascii=True, desc=i+": "):
        #For each character and for each font
        try:
            x=Image.new(mode="L",size=(30,30),color=255)
            #Create a new 30x30 image with the black and white mode
            draw=ImageDraw.Draw(x)
            #Create a drawing object for the image
            if j<=len(fontlist)-1:
                fontchoice=fontlist[j]
            #Set the font to the one being cycled through in the list
            else:
                fontchoice=random.choice(fontlist)
            #Choose a random font for the last 500 items (for validation)
            font=ImageFont.truetype("Fonts/"+fontchoice,size=28+(random.randint(-4,2)))
            #Choose a random font size between 24 and 30
            w,h=font.getsize(i)
            draw.text(((30-w+random.randint(-10,10))//2,(30+random.randint(-10,0)-h)//2),i,fill=0,font=font)
            #Add the text to the centre of the image, with an x offset between -10 and 10
            #and a y offset between -10 and 0
            angle=random.randint(-15,15)
            if angle<0:
                angle=360+angle
            x=x.rotate(angle,fillcolor=255)
            #Rotate by a random angle between -15 and 15
            x=np.array(x)
            _,thresholded=cv2.threshold(x,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            x=Image.fromarray(thresholded)
            #Threshold the image using Otsu's method
            x=x.filter(ImageFilter.SMOOTH_MORE)
            #Smooth the image
            if j<=len(fontlist)-1:
                x.save("train/"+i+"_"+str(j)+".png")
            else:
                x.save("valid/"+i+"_"+str(j)+".png")
            #Save the last 500 items to the valid data folder
            #and all the others go to the train data folder
        except:
            pass
        #Try except loop in the case of errors with reading fonts
        #prevents program from stopping if one font is broken
