import json
import os
import sys
import random

def annotaions_preprocessing(per_an_data, an_num, num):
    per_an_data["id"] = an_num
    an_num += 1
    per_an_data["image_id"] = num
    return per_an_data, an_num

def data_insert(pre_data, an_idxing_data, data, start_idx, end_idx, num, an_num, idx_list, version):
    temp_idx_list = idx_list[start_idx:end_idx]
    for idx in temp_idx_list:
        i = pre_data["images"][idx]
        if an_idxing_data.get(i["id"]):
            for j in an_idxing_data[i["id"]]:
                if version == '2':
                    if not j["segmentation"]:
                        per_an_data, an_num = annotaions_preprocessing(j, an_num, num)
                        data["annotations"].append(per_an_data)
                elif version == '1':
                    if j["segmentation"]:
                        per_an_data, an_num = annotaions_preprocessing(j, an_num, num)
                        data["annotations"].append(per_an_data)
                elif version == '0':
                    per_an_data, an_num = annotaions_preprocessing(j, an_num, num)
                    data["annotations"].append(per_an_data)
        i["id"] = num
        num += 1
        data["images"].append(i)
         # test
#        if i["id"] == 2:
#            print(json.dumps(data))
#            break
    return data, num, an_num

def file_write(head, train_data, val_data, test_data):

    with open(head+'_train.json', 'w') as fp:
        json.dump(train_data, fp)
    with open(head+'_val.json', 'w') as fp:
        json.dump(val_data, fp)
    with open(head+'_test.json', 'w') as fp:
        json.dump(test_data, fp)

def main():

    version = sys.argv[1]
    
#    jpg_idx = dict.fromkeys(os.listdir('./images'), True)
    jpg_idx = dict.fromkeys(os.listdir('../../deetas/images'), True)

    # output
    train_data = {"images":[],"annotations":[]}
    val_data = {"images":[],"annotations":[]}
    test_data = {"images":[],"annotations":[]}
        
    train_number = 0
    val_number = 0
    test_number = 0
    annotation_train_number = 0
    annotation_val_number = 0
    annotation_test_number = 0
    # path read
    with open('./path','r') as p:         
        # files read 
        files = p.read().split("\n")[:-1]
        for file_path in files:
            with open(file_path,'r') as f:
                f_line = f.readline()
                json_data = json.loads(f_line)
        
                if train_number == 0:
                    train_data["categories"] = json_data["categories"]
                    val_data["categories"] = json_data["categories"]
                    test_data["categories"] = json_data["categories"]

                # annotations indexing
                annotation_idx_data = {}
        
                for i in json_data["annotations"]:
                    if not annotation_idx_data.get(i["image_id"]):
                        annotation_idx_data[i["image_id"]] = []
                    annotation_idx_data[i["image_id"]].append(i)
                
                for j in json_data["images"]:
                    if not jpg_idx.get(j['file_name']):
                        json_data['images'].remove(j)

                # data shuffle
                total_idx = len(json_data["images"])
                total_idx_list = list(range(total_idx))
                random.shuffle(total_idx_list)
                
                # find index
                test_idx = int(total_idx*0.9)
                val_idx = int(total_idx*0.8)
    
                train_data, train_number, annotation_train_number = data_insert(json_data, annotation_idx_data, train_data, 0, val_idx, train_number, annotation_train_number, total_idx_list, version)
                val_data, val_number, annotation_val_number = data_insert(json_data, annotation_idx_data, val_data, val_idx, test_idx, val_number, annotation_val_number, total_idx_list, version)
                test_data, test_number, annotation_test_number = data_insert(json_data, annotation_idx_data, test_data, test_idx, total_idx, test_number, annotation_test_number, total_idx_list, version)

    print(len(train_data["annotations"]), len(val_data["annotations"]), len(test_data["annotations"]))
    
    if version == '0':
        file_write("total", train_data, val_data, test_data)
    elif version == '1':
        file_write("seg", train_data, val_data, test_data)
    elif version == '2':
        file_write("not_seg", train_data, val_data, test_data)
    
    
main()
