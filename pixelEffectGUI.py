import cv2
import numpy as np

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

# set dimensions of the video feed
WIDTH, HEIGHT = 800, 600 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# default parameters
cell_size = 12 
circle_fill = 1
enable_red = 1
enable_green = 1
enable_blue = 1

# default callback function for createTrackBar
def nothing(x):
    pass

cv2.namedWindow('Controls')

#trackbars for grid size and circle fill
cv2.createTrackbar('Cell Size', 'Controls', cell_size, 50, nothing) #max 50
cv2.createTrackbar('Circle Fill', 'Controls', circle_fill, 1, nothing) # 0 unfilled, 1 filled

#color trackbars
cv2.createTrackbar('Red Channel', 'Controls', enable_red, 1, nothing)
cv2.createTrackbar('Green Channel', 'Controls', enable_green, 1, nothing)
cv2.createTrackbar('Blue Channel', 'Controls', enable_blue, 1, nothing)


#effect function to modify webcam feed
#parameter: input video frame
def effect(image, cell_size, circle_fill, enable_red, enable_green, enable_blue): 

    #creating a black window of the same size as the video frame
    global black_window
    black_window = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

    # define default grid size for pixelation effect 
    new_width, new_height = int(WIDTH/cell_size), int(HEIGHT/cell_size) #number of cells in the reduced resolution image
    
    #resize the image to a lower resolution (pixelated version)
    small_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST) #INTER_NEAREST ensures sharp resizing without smoothing
    circle_radius = max(1, cell_size//2)

    #loop through each cell in the reduced image
    for i in range(new_height):
        for j in range(new_width):
            # extract color channels of current "pixel/cell" in the reduced image
            color = small_image[i,j]
            B = int(color[0]) if enable_blue else 0
            G = int(color[1]) if enable_green else 0
            R = int(color[2]) if enable_red else 0

            #calculate coordinates for the circle on the original sized canvas
            coordinates = (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2)

            #place the circle at the center of each grid cell, 
            # draw a filled circle with the corresponding color on the black canvas
            # radius of the circle is set to 5 pixels, -1 indicates the circle is filled
            cv2.circle(black_window, coordinates, circle_radius, (B,G,R), -1 if circle_fill else 1)



while True:
    _, frame = cap.read()

    cell_size = max(1, cv2.getTrackbarPos('Cell Size', 'Controls'))
    circle_fill = cv2.getTrackbarPos('Circle Fill', 'Controls')
    enable_red = cv2.getTrackbarPos('Red Channel', 'Controls')
    enable_green = cv2.getTrackbarPos('Green Channel', 'Controls')
    enable_blue = cv2.getTrackbarPos('Blue Channel', 'Controls')

    effect(frame, cell_size, circle_fill, enable_red, enable_green, enable_blue)
    cv2.imshow('result', black_window)

    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

