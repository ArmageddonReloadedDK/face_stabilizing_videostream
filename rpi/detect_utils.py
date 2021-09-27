import torchvision.transforms as transforms
import cv2
import numpy as np
from rpi.coco_names import COCO_INSTANCE_CATEGORY_NAMES as coco_names

# this will help us create a different color for each class
COLORS = np.random.uniform(0, 255, size=(len(coco_names), 3))
# define the torchvision image transforms
transform = transforms.Compose([
    transforms.ToTensor(),
])


def predict(image, model, device, detection_threshold):
    # transform the image to tensor
    image = transform(image).to(device)
    image = image.unsqueeze(0)  # add a batch dimension
    outputs = model(image)  # get the predictions on the image
    # get all the predicited class names
    pred_classes = [coco_names[i] for i in outputs[0]['labels'].cpu().numpy()]
    # get score for all the predicted objects
    pred_scores = outputs[0]['scores'].detach().cpu().numpy()
    # get all the predicted bounding boxes
    pred_bboxes = outputs[0]['boxes'].detach().cpu().numpy()
    # get boxes above the threshold score
    boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)
    return boxes, pred_classes, outputs[0]['labels']


def draw_boxes(boxes, classes, labels, image):
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    for i, box in enumerate(boxes):
        color = COLORS[labels[i]]
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            color, 2
        )
        cv2.putText(image, classes[i], (int(box[0]), int(box[1] - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2,
                    lineType=cv2.LINE_AA)
    return image


def grid(image, nx, ny):
    shape = image.shape
    x_step = shape[0] // nx
    y_step = shape[1] // ny
    grid = np.zeros(shape)

    label = 0
    flag = True
    x = 0
    y = 0
    while flag:
        while x < (label + 1) * x_step:
            grid[x, y] = label
            x+=1
            if x%x_step==0:
                x=label*x_step
                y+=1
                if y%y_step==0:
                    label


