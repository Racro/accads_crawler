import torch
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import faiss
import numpy as np
import os
import json

#Define a function that normalizes embeddings and add them to the index
def add_vector_to_index(embedding, index):
    #convert embedding to numpy
    vector = embedding.detach().cpu().numpy()
    #Convert to float32 numpy
    vector = np.float32(vector)
    #Normalize vector: important to avoid wrong results when searching
    faiss.normalize_L2(vector)
    #Add to index
    index.add(vector)

def generate_vectors(images, extn):
    #load the model and processor
    device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
    processor = AutoImageProcessor.from_pretrained('facebook/dinov2-small')
    model = AutoModel.from_pretrained('facebook/dinov2-small').to(device)
                
    #Create Faiss index using FlatL2 type with 384 dimensions as this
    #is the number of dimensions of the features
    index = faiss.IndexFlatL2(384)

    import time
    t0 = time.time()
    for image_path in images:
        # print(time.time())
        img = Image.open(image_path).convert('RGB')
        with torch.no_grad():
            inputs = processor(images=img, return_tensors="pt").to(device)
            outputs = model(**inputs)
        features = outputs.last_hidden_state
        add_vector_to_index( features.mean(dim=1), index)

    print('Extraction done in :', time.time()-t0)

    #Store the index locally
    faiss.write_index(index, f"{extn}.index")

    #Store the image filepaths
    json.dump(images, open(f'{extn}_images.json', 'w'))