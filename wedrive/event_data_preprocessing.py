#-*- coding: utf-8 -*-
'''
작성일 : 2020-09-16
작성자 : 정성모
코드 개요 :
    교통방송 접수현황 데이터의 전처리 과정으로 제보유형의 도로상태 원활, 각종 행사, 기상정보에는
    이벤트 발생이 되지 않아 제거. 제보 유형인 기타항목의 내용 부분을 볼때, 안내의 대한 정보도 이벤트
    접수의 대한 데이터와 부적절함으로 제거
    
'''

import numpy as np
import pandas as pd
import re
import os

def main():
    files = os.listdir('./data')
#    l = [i for i in range(10)]
    for f in files:
        data = preprocessing('./data/'+f)
        data.to_excel('./preprocessing_data/'+f)

def preprocessing(file_path):
    '''
    함수개요 : 이벤트 접수의 의미 없는 데이터 제거(제보유형:원활,행사,기상 정보/내용:(안내)부분)
    파라미터 :
        file_path = 이벤트 접수 데이터 파일 위치
    '''
    df = pd.read_excel(file_path, header = 9)
    df = df.dropna(how = 'all')
    data = df.copy()
    data = data[data['제보유형']!='원활']
    data = data[data['제보유형']!='행사']
    data = data[data['제보유형']!='기상']
    data = data[data['내용'].str.startswith('(안내)')==False]
    data.reset_index(drop=True, inplace=True)
    
    return data

main()
