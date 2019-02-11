def overlay_boxes(boxes,image):
# Overlay the detected box on the image. It directly modifies the raw images
# so it should only be used for showing the graph.
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        image[x1:x1+5,y1:y2+1,:] =0
        image[x2:x2+5,y1:y2+1,:] =0
        image[x1:x2+1,y1:y1+5,:] =0
        image[x1:x2+1,y2:y2+5,:] = 0
        image[x1:x1+5,y1:y2+1,0] = 255
        image[x2:x2+5,y1:y2+1,0] = 255
        image[x1:x2+1,y1:y1+5,0] = 255
        image[x1:x2+1,y2:y2+5,0] = 255
