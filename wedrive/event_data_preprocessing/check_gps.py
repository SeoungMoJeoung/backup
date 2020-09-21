#-*- coding: utf-8 -*-
'''
작성일 : 2020-09-16
작성자 : 정성모
코드 개요 : 카카오 로컬 rest api 이용하여 주소를 입력하여 좌표를 구함
'''
import requests

def Convert_address_to_coordinates():
    '''
    함수개요 : 주소를 입력하면 그 주소의 맞는 위도 경도 값을 출력
    '''
    print("주소를 입력하시요.")
    searching = input()

    url = "https://dapi.kakao.com/v2/local/search/address.json?query={}".format(searching)
    headers = {
        "Authorization": "KakaoAK 3cf004a43127265d4b81715524a7c380"
    }
    places = requests.get(url, headers = headers).json()['documents']
    x = places[0]["x"]
    y = places[0]["y"]
    print(y, x)

Convert_address_to_coordinates()
