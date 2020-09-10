# Block_IO_linear_model

## BIO_01_linear_model_test
```
Block event 데이터가 없어 flow 데이터를 통해 먼저 네트워크를 생성하고 학습을 통해 예측한 데이터와 실제 데이터의 차이를 구함.
```
## BIO_02_linear_model
```
독립변수 : Size of IO, streamid, block_bio_queue, block_getrq, nvme_sq
종속변수 : block_rq_complete
데이터를 통해 먼저 네트워크를 생성하고 학습을 통해 예측한 데이터와 실제 데이터의 차이를 구함.
```
## BIO_03_linear_model_MyPreprocessing
```
독립변수 : Size of IO, streamid, block_bio_queue, block_getrq, nvme_sq
종속변수 : block_rq_complete
각 독립변수의 최솟값을 원 데이터에서 뺀 데이터를 학습데이터로 사용
```
## BIO_03_linear_model_MyPreprocessing
```
독립변수 : Size of IO, streamid, block_bio_queue, block_getrq, nvme_sq
종속변수 : block_rq_complete
각 독립변수의 최솟값을 원 데이터에서 뺀 데이터를 학습데이터로 사용
```
## BIO_04_linear_model_RelativeData_Extract
```
block_bio_queue, block_getrq, nvme_sq, block_rq_complete을 상대시간으로 변경
```
## BIO_05_linear_model_norm_std
```
독립변수 : Sector, block_bio_queue, block_getrq, nvme_sq
종속변수 : block_rq_complete
block_bio_queue, block_getrq, nvme_sq, block_rq_complete을 상대시간으로 변경
독립변수/종속변수 정규화, 표준화 하여 여러 test 진행
```
## BIO_06_linear_model_Per_Second_Count
```
독립변수 : Sector, block_bio_queue, block_getrq, nvme_sq, count_bbq, count_bg, count_ns, count_brc
종속변수 : block_rq_complete
block_bio_queue, block_getrq, nvme_sq, block_rq_complete을 상대시간으로 변경
BIO 사이클의 3개의 이벤트 데이터, Sector, 초당 BIO 이벤트의 갯수를 이용하여 RG_COMPLETE 데이터 예측
```
## BIO_07_linear_model_Pre_Row
```
독립변수 : Sector, block_bio_queue, block_getrq, nvme_sq, 이전 row들의 값들을 컬럼에 추가
종속변수 : block_rq_complete
block_bio_queue, block_getrq, nvme_sq, block_rq_complete을 상대시간으로 변경
BIO 사이클의 3개의 이벤트 데이터, Sector, 이전 row 데이터들을 이용하여(5, 8, 10개 rows) RG_COMPLETE 데이터 예측
```