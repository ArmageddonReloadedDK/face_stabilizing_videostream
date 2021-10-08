import torchvision
import torch
import cv2
import detect_utils as detect_utils
from PIL import Image


# define the computation device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# load the model
model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(pretrained=True)
# load the model on to the computation device
model.eval().to(device)

# read the image and run the inference for detections
image = Image.open('me2.JPG')
boxes, classes, labels = detect_utils.predict(image, model, device, 0.7)
image = detect_utils.draw_boxes(boxes, classes, labels, image)
cv2.imshow('Image', image)
new_img_name='new_img'
cv2.imwrite(f"outputs/{new_img_name}.jpg", image)
cv2.waitKey(0)