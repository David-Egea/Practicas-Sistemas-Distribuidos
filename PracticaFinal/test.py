import pathlib
from utils.job import Job
import os

from client_files.client import Client
from server_files.server import Server
from slave_files.slave import Slave

from zipfile import ZipFile

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

# def test_image_task_module():
#     image_task_module = ImageTaskModule()
#     images = []
#     for i in range(0,9):
#         img_name = f"airplane_000{i}"
#         image = cv2.imread(f"{PATH}\\PracticaFinal\\Server\\fliesToDo\\{img_name}.jpg")
#         cv2.imshow(img_name, image)
#         cv2.waitKey(200)
#         cv2.destroyWindow(img_name)
#         images.append(image)
#     image_task_module.load_images(images)
#     response = image_task_module.do_task()
#     for i, img in enumerate(response):
#         cv2.imshow(f"airplane 000{i}", img)
#         cv2.waitKey(200)
#         cv2.destroyWindow(f"airplane 000{i}")
#     image_task_module.clear()
#     response = image_task_module.do_task()
#     print(response)

# def test_yolo_task_module():
#     yolo_module = Yolov5TaskModule()
#     images = []
#     for i in range(0,9):
#         img_name = f"drone_{i}"
#         image = cv2.imread(f"{PATH}\\PracticaFinal\\images\\{img_name}.jpg")
#         cv2.imshow(img_name, image)
#         cv2.waitKey(200)
#         cv2.destroyWindow(img_name)
#         images.append(image)
#     yolo_module.load_images(images)
#     response = yolo_module.do_task()
#     for i, r in enumerate(response):
#         cv2.imshow(f"drone_{i}", r[1])
#         cv2.waitKey(0)
#         cv2.destroyWindow(f"drone_{i}")

# def test_master_node():
#     # Creates a master node
#     master = MasterNode()
#     master.start()

def test_job_class():
    # Creates a new job
    job = Job(client_id="A", job_type="process.image.color_to_gray", payload = [])
    print(job.payload)
    print(job.done)
    job.payload = ["image0","image1","image2"]
    print(job.payload)

def test_client() -> None:
    # Creates a client
    client = Client()

def test_server() -> None:
    # Creates a server
    server = Server()
    server.start()

def test_slave() -> None:
    # Creates a slave node
    slave = Slave()
    slave.start()

def prepare_client_zip() -> None:
    """ Prepares a zip with all the required files for a client node."""
    client_zip = ZipFile("client_node.zip","w")
    # Includes the necessary files
    client_zip.write(os.path.join(FILE_PATH,'client_files','client.py'))
    client_zip.write(os.path.join(FILE_PATH,'client_files','client_config.ini'))
    client_zip.write(os.path.join(FILE_PATH,'client_files','Dockerfile'))
    client_zip.write(os.path.join(FILE_PATH,'client_files','requirements.txt')) # TODO: Revisar path del requirements del client
    client_zip.write(os.path.join(FILE_PATH,'configuration','configuration.py'))
    client_zip.write(os.path.join(FILE_PATH,'utils','job.py'))
    # Closes the zip object
    client_zip.close()

if __name__ == "__main__":
    # --- IMAGE TASK MODULE TEST ---
    # test_image_task_module()

    # --- YOLOV5 TASK MODULE TEST ---
    # test_yolo_task_module()

    # --- MASTER NODE TEST ---
    # test_master_node()

    # --- JOB CLASS TEST ---
    # test_job_class()

    # --- CLIENT CLASS TEST ---
    # test_client()

    # --- CLIENT ZIP TEST --- 
    # prepare_client_zip()

    # --- SERVER CLASS TEST ---
    # test_server()

    # --- SLAVE CLASS TEST ---
    test_slave()

    print("end test")
