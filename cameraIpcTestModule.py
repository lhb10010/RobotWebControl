#cameraIpcTestModule

image = "test1.jpg"

def getCurrentFrame():

    global image

    with open(image, "rb") as file:
        data = file.read()

    if image == "test1.jpg":
        image = "test2.jpg"
    else:
        image = "test1.jpg"

    return data

def initCamera():
    pass