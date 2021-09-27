import json

def data_insert(pre_data, an_idx_data, data, start_idx, end_idx, num, an_num):
    for i in pre_data["images"][start_idx:end_idx]:
        if an_idx_data.get(i["id"]):
            for j in an_idx_data[i["id"]]:
                j["id"] = an_num
                an_num += 1
                j["image_id"] = num
                data["annotations"].append(j)
        i["id"] = num
        num += 1
        data["images"].append(i)
#        if i["id"] == 2: #test
#            break
    return data, num, an_num

def main():
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
                
                # find index
                total_idx = len(json_data["images"])
                test_idx = int(total_idx*0.9)
                val_idx = int(total_idx*0.8)
    
                train_data, train_number, annotation_train_number = data_insert(json_data, annotation_idx_data, train_data, 0, val_idx, train_number, annotation_train_number)
                val_data, val_number, annotation_val_number = data_insert(json_data, annotation_idx_data, val_data, val_idx, test_idx, val_number, annotation_val_number)
                test_data, test_number, annotation_test_number = data_insert(json_data, annotation_idx_data, test_data, test_idx, total_idx, test_number, annotation_test_number)

    print(len(train_data["annotations"]), len(val_data["annotations"]), len(test_data["annotations"]))
    '''
    with open('train.json', 'w') as fp:
        json.dump(train_data, fp)
    with open('val.json', 'w') as fp:
        json.dump(val_data, fp)
    with open('test.json', 'w') as fp:
        json.dump(test_data, fp)
    '''
main()
