# Image Feature 분류 모델

- CNN의 과적합을 이용

## 목표

- 각 이미지 데이터들의 속성을 하나의 객체로 다루어, 객체들을 시공간 형태(공간을 나타내는 값)로 분류를 하는 것

## 개발환경

- Python (3.7 ver)
- CPU만 지원하는 Tensorflow 환경 (2.x ver)
- anaconda의 가상환경과 주피터를 이용 ( ver)

## CNN의 과적합을 이용

- CNN의 과적합이 일어나는 조건
  1. 학습의 반복횟수를 증가
  2. 필터 수를 증가 시켜 많은 가중치 값으로
  3. batch size를 낮춰 데이터 하나당 학습 될 수 있도록 함

- data.out 파일을 이용하여 test
  - 종속변수 : 이미지 속성 (파티션 ID, Idistance Key, 참조점으로부터 거리)
  - 독립변수 : 공간을 나타내는 임의의 값 (Random)
  - 여러가지 경우에서 test
    ```
    - 파라미터 개수 증가 test
    - Dense 레이어를 순차적으로 줄이며 test
    - MaxPooling 사용하여 test
    - ResNet을 이용하여 test
    ```
    
- src.txt 파일을 이용하여 test
  - 종속변수 : 이미지 속성 (특징 데이터 128차원)
  - 독립변수 : 공간을 나타내는 임의의 값 (Random)
  
## 실험

### 20.07.23  
src.txt의 DATA를 이용하여 실험 - accuracy 12%  
### 20.07.28
data.out의 DATA를 이용하여 기존 네트워크에 필터 갯수와 네트워크를 증가하여 실험 - accuracy : 10%  
data.out의 DATA를 이용하여 네트워크에서 Dense Layer의 필터 수를 적은 폭으로 줄이며 실험 - accuracy : 10%  
data.out의 DATA를 이용하여 기존 네트워크에 MaxPooling을 추가해서 실험 - accuracy : 10%  
### 20.07.30
data.out의 DATA를 이용하여 ResNet 네트워크 실험 - accuracy : 10%

- 정확도가 10% 정도로 너무 낮아 사용 할 수 없음. 종속변수와, 독립변수 사이의 연관성이 없으므로 학습을 잘 못하는 것으로 생각하고 있고  
  추후 Deeplearning을 이용하여 인덱싱 or 서치하는 논문 찾아 볼 것
