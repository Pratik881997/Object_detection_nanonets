import requests
import cv2
import json
import glob
import csv
import os
import subprocess

os.system('python Extract_details.py')
os.chdir(r'C:\Users\test1\PycharmProjects\final_object_detection')
subprocess.call(['ffmpeg', '-i', 'GH010034.mp4', '-vf', 'fps=1', 'scrn_shotz_10034/%d.png'])

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/a76b348b-2deb-4ebe-bec6-1afccdfab4c0/LabelFile/'

with open('Extracted_details.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

for image in glob.glob(r'scrn_shotz_10034/*.png'):

    img = image.split("\\")[1]
    count = img.split(".")[0]
    frame = cv2.imread(image,0)
    _, img_encoded = cv2.imencode('.png', frame)

    response = requests.post(
        url, auth=requests.auth.HTTPBasicAuth('c3ReeYwQXwHhb0FZcYk0-liOq4NkcVMw', ''),
        files={"file": ("frame.jpg", img_encoded.tostring())},
    )

    response = json.loads(response.text)
    print(str(count) + " " + image + " " + str(response))

    xmin = extract_values(response, 'xmin')
    ymin = extract_values(response, 'ymin')
    xmax = extract_values(response, 'xmax')
    ymax = extract_values(response, 'ymax')
    score = extract_values(response, 'score')

    bool_val = False

    try:
       for (i_xmin, i_ymin, i_xmax, i_ymax, i_score) in zip(xmin, ymin, xmax, ymax, score):
           if(i_score > 0.5):
                frame = cv2.rectangle(frame, (i_xmin, i_ymin), (i_xmax, i_ymax), (0, 0, 255), 2)
                bool_val = True

    except Exception as e:
        print(e)

    if(bool_val):
        count = int(count) + 1
        row = rows[count]
        lat_val = row[1]
        long_val = row[2]
        img_name = lat_val + "," + long_val + '.png'
        cv2.imwrite("Annotated_Images/" + img_name, frame)