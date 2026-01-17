import time, requests, numpy as np # The import time is so we can wait between the images, the requests is so we can download images from the internet, and finally the numpy is to work with images as the number arrays
from PIL import Image #this here imports image from the PIL to open image files 
from io import BytesIO # this was a little confusing but it imports BytesIO so we can treat the downloaded data like a file 

URL = "https://www.nps.gov/webcams-bost/ne-ts.jpeg" 
N = 10 #number of the images here
WAIT = 10 #seconds to wait between the images 
THRESH = 220 #this is the brightness threshold which is very bright pixels here 
MAXPTS = 400 # the max number of the bright points to track oer frame 

frames = [] #this is a list that stores all the image frames

for i in range(N): #the loop n times to download n images here
    print("Fetching frame", i+1) #this is the print progress so we know the progressis running 
    r = requests.get(URL + f"?t={time.time()}", timeout=10) # downlaoded the timestamp here and added a timestamp to avoid the catching
    img = Image.open(BytesIO(r.content)).convert("L") # open the downloaded image here and convert it to the greyscale
    arr = np.array(img)[:300, :] #converted the image of the numpy array of the pixel values and it keeps only the top part of the image which is the sky
    frames.append(arr) # saved this frame here in the list
    time.sleep(WAIT) #it waits before grabbing the next frame here 

def points(a): # this here finds bright points in an image 
    ys, xs = np.where(a > THRESH) #here it finds the pixel positions where the brightness is above the threshold 
    if len(ys) == 0: # here if there is not bright points found it returns an empty list here
        return []
    idx = np.random.choice(len(ys), size=min(MAXPTS, len(ys)), replace=False) # randomly select a limited number of points over here 
    return list(zip(ys[idx], xs[idx])) # this returns the y and x positions of the selected points 

motions = [] # this stores motion values between the frames and this is a list 

for i in range(1, N): # this compares each frame to the one before it 
    p1 = points(frames[i-1]) # this one gets bright points from the previous frame 
    p2 = points(frames[i]) # this gets bright points from the current frame 
    if not p1 or not p2: # this is saying if either frame has no points then it will skip it 
        continue
    dists = [] # this here store distances from between matchung points
    for y1, x1 in p1: #this is for each point oif the first frame 
        d = min(((y1-y2)**2 + (x1-x2)**2)**0.5 for y2, x2 in p2) # finds the closest point of the next frame
        dists.append(d)
    motions.append(np.mean(dists)) # this saves the average motion ofr the frame pair 

print("Avg motion (px):", np.mean(motions) if motions else "no data") # finally prints the average motion of across all frames here 