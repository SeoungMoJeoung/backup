'''
    작성 : 정성모
    용도 : 클립 별 json 데이터 전처리(annotation 된 json 데이터로부터 track_id를 기준으로 필요한 데이터들 추출)
    출력 : 파일별 track id 기준의 데이터
'''

import json
import sys
import os
import random

def main():
    # select fuction
    version = sys.argv[1]

    # define json dict
    data = {}
        
    # define raw json path
    json_paths = "./json"
    json_files_list = os.listdir(json_paths)

    # define out path
    output_path = "./output"

    # preprocessing
    for json_file_name in json_files_list:
        json_file = os.path.join(json_paths, json_file_name)
        print("preprocessing :", json_file)
        data[json_file_name] = {"track":[]}
        with open(json_file,'r') as json_reader:
            file_line = json_reader.readline()
            try:
                json_data = json.loads(file_line)
            except:
                print("error")
                continue
            
            data[json_file_name] = track_insert(json_data, data[json_file_name])
        break  #test용
    '''
    if version == '0':
        file_write(output_path , data)
        print("whole_data")
    '''
def track_insert(json_data, data):
    temp = {}
    for an_data in json_data["annotations"]:
        if an_data["attributes"].get("track_id"):
            track_id = an_data["attributes"]["track_id"]
            if not temp.get(track_id):
                temp[track_id] = {"id":an_data["attributes"]["track_id"],"category_id":an_data["category_id"],"annotations":[{"bbox":an_data["bbox"],"segmentation":an_data["segmentation"],"Status":an_data["attributes"]["Status"]}]}
            else:
                temp[track_id]["annotations"].append({"bbox":an_data["bbox"],"segmentation":an_data["segmentation"],"Status":an_data["attributes"]["Status"]})
           
    for t_id in temp:
        data["track"].append(temp[t_id])
    return data

def file_write(head, data):

    with open(head+'/train.json', 'w') as fp:
        json.dump(data, fp)


main()
