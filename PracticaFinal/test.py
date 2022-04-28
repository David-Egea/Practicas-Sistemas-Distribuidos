import cv2
from task_modules.yolov5_task_module import Yolov5TaskModule
from task_modules.image_task_module import ImageTaskModule
from node_files.master_node import MasterNode
import pathlib

PATH = str(pathlib.Path().resolve())

def test_image_task_module():
    image_task_module = ImageTaskModule()
    images = []
    for i in range(0,9):
        img_name = f"airplane_000{i}"
        image = cv2.imread(f"{PATH}\\PracticaFinal\\Server\\fliesToDo\\{img_name}.jpg")
        cv2.imshow(img_name, image)
        cv2.waitKey(200)
        cv2.destroyWindow(img_name)
        images.append(image)
    image_task_module.load_images(images)
    response = image_task_module.do_task()
    for i, img in enumerate(response):
        cv2.imshow(f"airplane 000{i}", img)
        cv2.waitKey(200)
        cv2.destroyWindow(f"airplane 000{i}")
    image_task_module.clear()
    response = image_task_module.do_task()
    print(response)

def test_yolo_task_module():
    yolo_module = Yolov5TaskModule()
    images = []
    for i in range(0,9):
        img_name = f"drone_{i}"
        image = cv2.imread(f"{PATH}\\PracticaFinal\\images\\{img_name}.jpg")
        cv2.imshow(img_name, image)
        cv2.waitKey(200)
        cv2.destroyWindow(img_name)
        images.append(image)
    yolo_module.load_images(images)
    response = yolo_module.do_task()
    for i, r in enumerate(response):
        cv2.imshow(f"drone_{i}", r[1])
        cv2.waitKey(0)
        cv2.destroyWindow(f"drone_{i}")

def test_master_node():
    # Creates a master node
    master = MasterNode()
    master.start()

if __name__ == "__main__":
    # --- IMAGE TASK MODULE TEST ---
    # test_image_task_module()
    # --- YOLOV5 TASK MODULE TEST ---
    # test_yolo_task_module()
    # --- MASTER NODE TEST ---
    test_master_node()
