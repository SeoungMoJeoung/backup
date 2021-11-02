'''
    작성 : 정성모
    용도 : 클립 별 json 데이터 전처리(annotation 된 json 데이터로부터 track_id를 기준으로 필요한 데이터들 추출)
    출력 : 파일별 track id 기준의 데이터
'''

import pickle
import json
import sys
import os
import random

def main():
    # select fuction
    version = sys.argv[1]
    bbox_num = sys.argv[2]

    # define data
    train_data = []
    val_data = []
    test_data = []

    # define raw json path
    json_paths = "./json"
    json_files_list = os.listdir(json_paths)

    # define out path
    output_path = "./output"

    # preprocessing
    for json_file_name in json_files_list:
        json_file = os.path.join(json_paths, json_file_name)
        print("preprocessing :", json_file)
        with open(json_file,'r') as json_reader:
            file_line = json_reader.readline()
            try:
                json_data = json.loads(file_line)
            except:
                print("error")
                continue
            
            track_info = extract_track_info(json_data)

            data = create_input(track_info, int(bbox_num))

            # data shuffle
            random.shuffle(data)

            # data divide
            total_idx = len(data)
            test_idx = int(total_idx*0.9)
            val_idx = int(total_idx*0.8)
            
            train_data.extend(data[:val_idx])
            val_data.extend(data[val_idx:test_idx])
            test_data.extend(data[test_idx:])
         
#        break  #test용

    print("train :", len(train_data))
    print("val :", len(val_data))
    print("test :", len(test_data))

    if version == '0':
        file_write(output_path , train_data, val_data, test_data)
        print("whole_data")
    

def extract_track_info(json_data):

    temp = {}
    for an_data in json_data["annotations"]:
        if an_data["attributes"].get("track_id"):
            track_id = an_data["attributes"]["track_id"]
            if not temp.get(track_id):
                temp[track_id] = {"id":an_data["attributes"]["track_id"],"category_id":an_data["category_id"],"annotations":[{"bbox":an_data["bbox"],"segmentation":an_data["segmentation"],"Status":an_data["attributes"]["Status"]}]}
            else:
                temp[track_id]["annotations"].append({"bbox":an_data["bbox"],"segmentation":an_data["segmentation"],"Status":an_data["attributes"]["Status"]})
           
    return temp

def create_input(track_info, num):

    data = []
    for track_idx in track_info:
        track_lng = len(track_info[track_idx]["annotations"])
        if track_lng < num:
            continue
        for i in range(track_lng-num+1):
            temp = [track_info[track_idx]["annotations"][i+num-1]["Status"], track_info[track_idx]["category_id"]]
            for j in range(i,num+i):

                temp.append(track_info[track_idx]["annotations"][j]["bbox"])
            data.append(temp)
    return data

def file_write(head, tr_d, v_d, ts_d):

    with open(head+'/train.pickle', 'wb') as ft:
        pickle.dump(tr_d, ft)
    with open(head+'/val.pickle', 'wb') as fv:
        pickle.dump(v_d, fv)
    with open(head+'/test.pickle', 'wb') as fs:
        pickle.dump(ts_d, fs)


main()
