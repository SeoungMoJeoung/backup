# YOLOv4_Data 전처리

MSCOCO 2017은 YOLOv4에 사용되는 데이터로써 NIA과제로부터 얻은 데이터 전처리 작업(이미지 데이터는 구글드라이브)

---

## NIA_an_data_ver1.py

- 여러 path에 있는 json 데이터들을 통합하여 train/val/test(8:1:1)로 split
- json 데이터의 속성인 image, annotations들의 Idx 및 ID 조정

## NIA_an_data_ver1.py

- ver1 방법에 shuffle 적용한후 train/val/test(8:1:1)로 split
- `json_data["annotations"]["segmentation"]`의 값이 "존재, 존재X, 존재+존재X" 3가지 타입의 train/val/test data 생성

## NIA_image_data.py

- 한 곳에 모여있는 이미지 데이터들을 train/val/test 별로 분류 (하지만, 한 파일에 있어도 상관없으므로 더 이상 업데이트 X)
- image data는 구글 드라이버