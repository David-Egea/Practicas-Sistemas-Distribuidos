from typing import List, Dict, Any, Tuple
from Node.task_module import taskModule
import numpy as np
import cv2
import torch
from configuration.configuration import Configuration

class Yolov5TaskModule(taskModule):
    """ Task module child class. Performs a object detection on images using Yolov5. """

    def __init__(self) -> None:
        # Calls superclass constructor
        super().__init__(task="yolov5_processing")
        # Gets the yolov5 repository path from configuration
        yolo_rep_path = str(Configuration.get_config_param("Yolov5","yolo_rep_path"))
        # Gets the yolov5 weights path from configuration
        yolo_weights_path = str(Configuration.get_config_param("Yolov5","yolo_weights_path"))
        # Loads a custom model of yolo with indicated weights
        self._model = torch.hub.load(yolo_rep_path,'custom',path=yolo_weights_path,source='local', verbose=False)
        # Initializes the module stack
        self._img_stack = []

    def load_image(self, image: np.ndarray) -> None:
        """ Adds the passed image to the top of stack."""
        self._img_stack.append(image)

    def load_images(self, images: List[np.ndarray]) -> None:
        """ Adds the images to the stack."""
        for img in images:
            # Adds the image to the stack
            self.load_image(img)

    def clear(self) -> None:
        """ Clears all images at the stack."""
        self._img_stack.clear()

    def do_task(self) -> List[np.ndarray]:
        """ Performs the image procesing task."""
        # Defines an empty response
        response = []
        # Iterates for each image in the image stack
        for i in range(len(self._img_stack)):
            # Takes out the oldest image from the stack 
            img = self._img_stack.pop(0)
            # Carries outs the image processing task
            detection, img_proc = self._detect(img)
            # Adds the image to the response
            response.append((detection, img_proc))
        return response

    def _detect(self, image: np.ndarray) -> Tuple[List[Dict[str, Any]],np.ndarray]:
        """ Image processing method. """
        # Obtains image inference
        result = self._model(image)
        # Extracts x, y cordinates of detections
        result = result.pandas().xywh[0]
        # Sets the detection in dict format
        detection = [{"id": i, "name": result.name[i], "xc": result.xcenter[i], "yc": result.ycenter[i], "w": result.width[i], "h":result.height[i], "conf": result.confidence[i]} for i in range(len(result))]
        # Generates an output image
        output_img = image.copy()
        for obj in detection:
            # Cordinates of object
            p1 = (int(obj['xc']-obj['w']/2),int(obj['yc']-obj['h']/2))
            p2 = (int(obj['xc']+obj['w']/2),int(obj['yc']+obj['h']/2))
            # Marks the detection with a rectangle
            cv2.rectangle(output_img,p1,p2,(0,0,255),2)
            cv2.putText(output_img,f"{obj['name']}#{obj['id']}",(p1[0],int(obj["yc"])),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
        # Returns the detection and the output image
        return detection, output_img

if __name__ == "__main__":
    yolo_module = Yolov5TaskModule()
    images = []
    for i in range(0,10):
        img_name = f"airplane_000{i}"
        image = cv2.imread(f"C:\\Users\\egeah\\Sistemas Distribuidos\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\Server\\filesToDo\\{img_name}.jpg")
        cv2.imshow(img_name, image)
        cv2.waitKey(200)
        cv2.destroyWindow(img_name)
        images.append(image)
    yolo_module.load_images(images)
    response = yolo_module.do_task()
    for img in response:
        cv2.imshow(f"airplane 000{i}", img)
        cv2.waitKey(0)
