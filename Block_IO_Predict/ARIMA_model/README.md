# BIO_ARIMA_model

```
BIO_01_ARIMA.ipynb
```
Block event 데이터가 없어 flow 데이터를 통해 먼저 네트워크를 생성하고  
학습을 통해 예측한 데이터와 실제 데이터의 차이를 구함.

```
BIO_02_ARIMA_evaluation.ipynb
```
nvme_sq로 정렬하여 데이터 index 재생성, 원 데이터에서 complete 값이 0인  
row를 확인하고 해당 row에 nvme_sq를 0 값으로 변경

```
BIO_03_ARIMA_diff_evaluation.ipynb
```
getrq로 정렬하여 데이터 index 재생성, 원 데이터에서 complete – nvme_sq 값이 0인  
row를 확인하고 해당 row에 nvme_sq - getrq를 0 값으로 변경

```
BIO_04_ARIMA_diff_evaluation_data_process.ipynb
```
예측 데이터와 실제 데이터 차이 확인

```
BIO_05_ARIMA_data_visualization.ipynb
```
Arima로 예측한 데이터와 실제 데이터 시각화
