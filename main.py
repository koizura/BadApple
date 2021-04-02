from PIL import Image
import numpy as np
import cv2
import os

print("starting...")

gscale = "@%#*+=-:. "

def extractFrames(video, output):
    os.mkdir(output)
    cap = cv2.VideoCapture(video)
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        
        if(ret == True):
            cv2.imwrite(os.path.join(output, "frame{:d}.jpg".format(count)), frame)
            count += 1
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def getAverageL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w*h))

def convertToTxt(fileName, cols, scale):
    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale
    rows = int(H/h)

    aimg = []
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        if j == rows-1:
            y2 = H
        aimg.append("")
        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)
            if i == cols-1:
                x2 = W 
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            gsval = gscale[int((avg*9)/255)]
            aimg[j] += gsval
    return aimg

def main():
    frameSkip = 2
    for i in range(int(6571/frameSkip)):
        frame = i*frameSkip
        aimg = convertToTxt("./frames/frame"+str(frame)+".jpg", int(100), float(0.43))
        f = open("output.txt", 'w')
        for row in aimg:
            f.write(row + '\n')
        f.close()
                
#extractFrames("Bad Apple!!.mp4", "frames")
main()