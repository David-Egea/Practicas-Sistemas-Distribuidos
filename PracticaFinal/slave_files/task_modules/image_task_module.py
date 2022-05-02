from typing import List
from task_modules.task_module import TaskModule
import numpy as np
import cv2

class ImageTaskModule(TaskModule):
    """ Task module child class. Performs image range transformation from BGR to Gray colorscale. """

    def __init__(self) -> None:
        # Calls superclass constructor
        super().__init__(task="image_processing")
        # Initializes the module stack
        self._img_stack = []

    def load_image(self, image: np.ndarray) -> None:
        """ Adds the passed image to the top of stack."""
        self._img_stack.append(image)

    def load_images(self, images) -> None:
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
            img_proc = self._process_image(img)
            # Adds the image to the response
            response.append(img_proc)
        return response

    def _process_image(self, image: np.ndarray) -> None:
        """ Image processing method. """
        # In this case the image is converted from BGR to Gray colorscale
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)