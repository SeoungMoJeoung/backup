import json
import shutil

def images_move(param):
    path = './' + param + '.json'
    with open(path, 'r') as f:
        pre_path = './image/train_images/'
        new_path = './image/' + param + '_images/'

        data = json.loads(f.read())
        for i in data["images"]:
            shutil.move(pre_path+i["file_name"], new_path+i["file_name"])

def main():
    images_move('val')
    images_move('test')

main()
