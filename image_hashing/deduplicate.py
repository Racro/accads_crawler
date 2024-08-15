import os
from detect_white import is_almost_white_page,is_almost_single_color
from faiss_compare import return_index
from faiss_vector_gen import generate_vectors
# import faiss
import subprocess
import time
from ocr import detect_text
import json

# def generate_index():
#     subprocess.call(["python3", "faiss_vector_gen.py", "--images", "control"])
#     time.sleep(2)
#     subprocess.call(["python3", "faiss_vector_gen.py", "--images", "adblock"])
#     time.sleep(2)

def remove_white_images(fpath):
    images = []
    for root, dirs, files in os.walk(fpath):
        for file in files:
            if file.endswith('png'):
                if not is_almost_single_color(root  + '/'+ file):
                    images.append(root  + '/'+ file)
    return images

def extract_text(images, extn):
    img_to_txt = {}
    no_txt_images = []
    for image in images:
        txt = detect_text(image)
        if txt == '':
            no_txt_images.append(image)
            continue
        img_to_txt[image] = txt
    json.dump(no_txt_images, open(f'no_txt_images_{extn}.json', 'w'))
    json.dump(img_to_txt, open(f'ocr_{extn}.json', 'w'))
    
    return list(img_to_txt.keys())

def remove_duplicates(images, vector_index, extn):
    # print(len(images), images)
    interesting_index = []

    for image in range(len(images)):
        d_ind, i_ind = return_index(images[image], vector_index)
        distance = list(d_ind[0])
        index = list(i_ind[0])
        
        try:
            for d in range(1, len(distance)):
                # print(f'distance[{d}]', distance[d])
                if distance[d] < 0.001:
                    if index[d] not in interesting_index and index[d] > image:
                        interesting_index.append(index[d])
        except Exception as e:
            print(e)

    if len(interesting_index) > 1:
        interesting_index.sort(reverse=True)
        print('interesting_index', len(interesting_index), interesting_index)
        for i in interesting_index:
            try:
                del images[i]
            except Exception as e:
                print(e, i)
                continue
    
    json.dump(images, open(f'images_dedup_{extn}.json', 'w'))

def adb_in_ctrl():
    adb_images = json.load(open('images_dedup_adb.json', 'r'))
    mapp = {}
    mapp['found'] = []
    mapp['not found'] = []

    for image in adb_images:
        distance, index = return_index(image, 'control.index')
        distance = distance[0]
        index = index[0]

        if distance[0] == 0:
            mapp['found'].append(image)
        else:
            mapp['found'].append(image)

    json.dump(mapp, open('adb_in_ctrl.json', 'w'))

adb_path = '../adblock/adshots'
control_path = '../control/adshots'
# adb_path = 'f2'
# control_path = 'f1'

control_index = 'control.index'
adb_index = 'adblock.index'

# remove whitespaces
control_images = remove_white_images(control_path)
adb_images = remove_white_images(adb_path)

# OCR
control_images = extract_text(control_images, 'control')
time.sleep(5)
adb_images = extract_text(adb_images, 'adblock')
time.sleep(5)

# control_images = list(json.load(open('ocr_control.json', 'r')).keys())
# adb_images = list(json.load(open('ocr_adblock.json', 'r')).keys())

# generate vectors
generate_vectors(control_images, 'control')
time.sleep(5)
generate_vectors(adb_images, 'adb')
time.sleep(5)

# deduplicates
remove_duplicates(control_images, 'control.index', 'control')
time.sleep(5)
remove_duplicates(adb_images, 'adb.index', 'adb')
time.sleep(5)

adb_in_ctrl()