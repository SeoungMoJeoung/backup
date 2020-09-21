# Web_Server

## 목표
- 지도의 원하는 지점의 좌표를 얻기 위해 서버 구축

## 개발이유
- Kakao 로컬 API의 REST API를 이용하여 간단하게 좌표를 가져오려 했으나,
- 주소로 나타나는 지도의 범위가 너무 크고 특정 지점(도로 위의 좌표)을 선택하기 어려움
- Kakao Maps API는 REST API가 없고, Javascript API 지원 하며, 여러 기능이 있어 서버 구축 하게 됨

## 개발환경
- Node.js (12.18.4 ver), npm (6.14.6 ver)
- Kakao Maps Javascript API

## 웹 서버 구축
- Express 프레임워크를 사용, express-generator 모듈이용, -e 옵션으로 ejs라는 View 엔진 사용(기본 jade)
- Kakao Maps API의 주소를 찾기, 선택 지점 좌표 얻기의 기능을 이용

## 문제점
- OPEN API 이여서 검색 횟수가 300,000번으로 한정

## 추가사황
```
node bin/www
```
서버 실행

```
210.119.145.34:3000
```
웹페이지 주소

```
views/index.ejs
```
웹 서버에서 GET으로 받을 때 처리 부분