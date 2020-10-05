'''
작성일 : 2020-10-01
작성자 : 정성모
코드 개요 : 
'''
import pandas as pd
import os

read_path = "./data/original_data/"

def main():
    '''
    함수 개요 :
    파라미터 :
    '''
    data = file_combine()
    per_count = 8000
    person = 10
    for i in range(person):
        name = str(i)
        data[per_count*i:per_count*(i+1)].to_excel("./data/preprocessing_data/"+name+".xlsx")
	

def file_combine():
    '''
    함수 개요 :
    파라미터 :
    '''
    data = pd.DataFrame()
    file_list = os.listdir(read_path)
    for i in file_list:
        temp = preprocessing(i)
        data = pd.concat([data,temp], ignore_index=True)
    data.sort_values(by=['접수번호'], axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data

def preprocessing(f):
    '''
    함수 개요 :
    파라미터 :
    '''
    data = pd.read_excel(read_path+f,header=9)
    data.dropna(how='all', inplace=True)
    data = data[data['제보유형']!='원활']
    data = data[data['내용'].str.startswith('(안내)') == False]
    data.reset_index(drop=True, inplace=True)
    return data

main()
