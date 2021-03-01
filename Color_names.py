import numpy as np
import pandas as pd
import argparse
import cv2

clicked=False
r=g=b=xpos=ypos=0

df=pd.read_csv("colors.txt",names=["color","color_name","hex","R","G","B"])

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
img = cv2.imread(img_path)

d={
    100:15,
    200:3,
    300:2,
    700:0.7,
    900:0.7,
    1500:0.5,
    3000:0.5,
    10000:0.3
}
for k,v in d.items():
    
    if img.shape[0]<=k or img.shape[1]<=k:
        img = cv2.resize(img,(0,0),fx=v,fy=v)
        break
        
        
def draw(event, x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        
def getColorName(df,R,G,B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R- int(df.loc[i,"R"])) + abs(G- int(df.loc[i,"G"]))+ abs(B- int(df.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = df.loc[i,"color_name"]
    return cname


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw)
while(1):
    cv2.imshow("image",img)
    if (clicked):
        cv2.rectangle(img,(20,20), (700,60), (b,g,r), -1)
        text = getColorName(df,r,g,b)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    
    if cv2.waitKey(20) & 0xFF == 27:
        break
        
    if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
        break  

cv2.destroyAllWindows()