from google.cloud import vision

## Initialisation
# gcloud init
# gcloud auth application-default login

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    ret = ''
    
    if texts == '':
        return ret    
    
    for text in texts:
        ret = ret + ' ' + text.description
    return ret

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )