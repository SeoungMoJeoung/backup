#-*- coding: utf-8 -*-

from haversine import haversine
from math import radians, sin, cos, degrees, atan2

# def trajectory2segment(traj, param_segment_index=0):

def trajectory2segment(param_segment_index=0, param_segments=[]):

    start_segment_index = 0 # 매핑할 세그먼트에 첫번재 포인트의 인덱스@@@@@@@@@@@@@@@ 0 값을 첫번째 GPS 값으로 바꿔줘야함
    end_segment_index = 0 # 매핑할 세그먼트에 마지막 포인트의 인덱스
    error_weight = 0 # 매핑 추정 과정에서 반복적으로 오류가 발견될 때 확인하는 변수
    count = 0 # 매핑 추정 과정의 리셋을 위한 카운터
    gps_index = 0 # 현재 GPS 인덱스
    segment_index = param_segment_index # 궤적이 지나는 세그먼트들 중에서 GPS 한점과 가장 가까운 세그먼트를 찾기위한 인덱스
    segments_index = 0 # 궤적이 지나는 세그먼트들의 인덱스
    contiune_index = -1
    pre_index = 0

    test_count = 0

    mapping = {} # 매핑된 데이터
    segments = param_segments # 궤적이 지나는 세그먼트들
    segment = [] # 궤적이 지나는 세그먼트들 중에 하나의 segment

    traj=[[37.438368742048006,126.61771557433434],[37.438486127245,126.61779407465104],[37.43864409371253,126.61788366852345],[37.43881562982121,126.6179901433133],[37.43893303308777,126.61807429427849],[37.439131598882184,126.61818063257748],[37.43928507831776,126.6182759006899],[37.43950180975253,126.61842734690836],[37.43971846806032,126.61855619472999],[37.43992162952108,126.61869076169923],[37.44014724282438,126.61880261574277],[37.44033251159104,126.61897682455667],[37.44060328362089,126.61912235101052],[37.44086519109965,126.61931312338258],[37.44107283846678,126.61944202169903],[37.441298632883075,126.61961037904919],[37.44154241060879,126.61976734631925],[37.44186277270862,126.61992392723678],[37.44205688630397,126.62004724727693],[37.44230066343473,126.62020421753198],[37.442512832931186,126.62033874801297],[37.44270705493798,126.62049597043651],[37.44294629021748,126.62064166611451],[37.44319001216001,126.6207816899005],[37.443411190934974,126.62091617813225],[37.443699980406606,126.62106162658358],[37.44390777068216,126.62123573561071],[37.444074762522945,126.62133094784448],[37.444264387738976,126.62145994797012],[37.444238009173404,126.62166348985025],[37.44411335204148,126.62212743723579],[37.44401494687969,126.62234829120838],[37.443925713626484,126.62261995056687],[37.44376915746497,126.6229710501706],[37.44363507110728,126.6233050850547],[37.4434602950676,126.62359412102587],[37.44336687755543,126.62396750116991]]

    data = {'type': 'Feature', 'properties': {'LINK_ID': '1610079300', 'F_NODE': '1610028900', 'T_NODE': '1610008100', 'LANES_': 2.0, 'ROAD_RANK_': '101', 'ROAD_TYPE_': '001', 'ROAD_NO_': '400', 'ROAD_NAME_': '제2외곽순환고속도로', 'ROAD_USE_': '0', 'MULTILINK': '0', 'CONNECT_': '000', 'MAX_SPD_': 100.0, 'REST_VEH_': '5', 'REST_W_': 0.0, 'REST_H_': 500.0, 'LENGTH': 2852.94926366, 'REMARK_': None}, 'geometry': {'type': 'MultiLineString', 'coordinates': [[[126.61757877687646, 37.43813620738528], [126.61770844328697, 37.43833006383382], [126.61969107789666, 37.44142800997755], [126.62175791338595, 37.44476824008163], [126.62304378090506, 37.44684617329508], [126.62511155083054, 37.450187378809865], [126.62539806961156, 37.450650580424366], [126.62741820578408, 37.45373924394933], [126.62813636955475, 37.45486908959261], [126.63023968088014, 37.458025529645965], [126.63046316646192, 37.458374261793615], [126.63066764130703, 37.45870793952353], [126.63082970574035, 37.458994914033134], [126.6310091266734, 37.459303997364444], [126.63199637424678, 37.461122068571]]]}}

    data_s = {'type': 'Feature', 'properties': {'LINK_ID': '1610013711', 'F_NODE': '1610028900', 'T_NODE': '1610091000', 'LANES_': 4.0, 'ROAD_RANK_': '104', 'ROAD_TYPE_': '000', 'ROAD_NO_': '-', 'ROAD_NAME_': '서해대로', 'ROAD_USE_': '0', 'MULTILINK': '0', 'CONNECT_': '000', 'MAX_SPD_': 70.0, 'REST_VEH_': '0', 'REST_W_': 0.0, 'REST_H_': 470.0, 'LENGTH': 356.989034385, 'REMARK_': '분할전ID_1610013701'}, 'geometry': {'type': 'MultiLineString', 'coordinates': [[[126.61752892709956, 37.43815740814351], [126.61936346035571, 37.44102201450388]]]}}

    data1 = {'type': 'Feature', 'properties': {'LINK_ID': '1610013712', 'F_NODE': '1610091000', 'T_NODE': '1610091300', 'LANES_': 4.0, 'ROAD_RANK_': '104', 'ROAD_TYPE_': '000', 'ROAD_NO_': '-', 'ROAD_NAME_': '서해대로', 'ROAD_USE_': '0', 'MULTILINK': '0', 'CONNECT_': '000', 'MAX_SPD_': 70.0, 'REST_VEH_': '0', 'REST_W_': 0.0, 'REST_H_': 470.0, 'LENGTH': 418.307165383, 'REMARK_': '분할전ID_1610013701'}, 'geometry': {'type': 'MultiLineString', 'coordinates': [[[126.61936346035571, 37.44102201450388], [126.61994827460897, 37.441935145313565], [126.62136587528953, 37.44424856831624], [126.62145969544505, 37.44439997172635]]]}}

    data2 = {'type': 'Feature', 'properties': {'LINK_ID': '1610240200', 'F_NODE': '1610091300', 'T_NODE': '1610092000', 'LANES_': 3.0, 'ROAD_RANK_': '107', 'ROAD_TYPE_': '000', 'ROAD_NO_': '-', 'ROAD_NAME_': '서해대로180번길', 'ROAD_USE_': '0', 'MULTILINK': '0', 'CONNECT_': '000', 'MAX_SPD_': 60.0, 'REST_VEH_': '0', 'REST_W_': 0.0, 'REST_H_': 0.0, 'LENGTH': 299.853125517, 'REMARK_': None}, 'geometry': {'type': 'MultiLineString', 'coordinates': [[[126.62137805689154, 37.444373321465044], [126.6244266336388, 37.44319400462685]]]}}
 
    if param_segment_index == 0:

#        segment = find_segment(traj[gps_index])
        segment.append(data)
        segment.append(data_s)
        segments.append(segment)

    s_gps = traj[gps_index] # 점과 점사이의 거리가 임계값을 넘어갔을 때, 이전 GPSㅡ
    p2s_distance = 999999999
    heading = False
    s_number = 0

    for gps in traj[1:]: # 수정 : index로 변경 해야함
        
        segment = []
        temp_segments = []
        gps_index = traj.index(gps) # 현재 GPS index
        if gps_index < contiune_index:

            contiune
        p2p_distance = min_distance(s_gps, gps)
        p2p_value = 10
        p2s_value = 20
        print(segments)
        print(segments_index, segment_index)
        if p2p_distance > p2p_value:  # GPS들의 거리를 먼저구해 임계값의 포함되면 아래와 같은 계산을 하지 않고 매핑
            segment_range = impute_segment_range(gps,
                                                 segments[segments_index][segment_index]['geometry']['coordinates'][0][0],
                                                 segments[segments_index][segment_index]['geometry']['coordinates'][0][-1])
            
            print("range",segment_range, gps_index)
            print("segments_index", segments_index)
            print(gps)
            if segment_range:
                
                for idx in range(s_number ,len(segments[segments_index][segment_index]['geometry']['coordinates'][0])-1):
                    print(idx) 
                    within_range = impute_segment_range(gps,
                                                        segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                                        segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])
                    if within_range:
                    
                        p2s_distance = min_distance(gps, gps,
                                                    segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                                    segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])

                        print("point to segemint distance : ",p2s_distance)
                        heading = bearing(s_gps, gps,
                                          segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                          segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])
                        
                        s_number = idx
                        break
                    
            elif not segment_range:
            
#                segment, contiune_index, pre_index = next_segments(segments[segments_index][segment_index][link_id], gps, gps_index, count) # 다음 새그먼트를 현재 새그먼트로 변환, count : 임계 값
#                segments.append(segment)
                print("범위를 넘음")

                if test_count == 0:
                    segment.append(data1)
                else:
                    segment.append(data2)

                test_count = test_count+1
                print("test_count",test_count)

                temp_segments.append(segment)
                s_number = 0
                tmep_segment_index = 0
                temp_segments_index = 0

                print(temp_segments)

                if segment_index != 0:
                   temp_segment_index = segment_index
                   segment_index = 0

                if segments_index != 0:
                   temp_segments_index = segments_index
                   segments_index = 0

                for idx in range(s_number ,len(temp_segments[segments_index][segment_index]['geometry']['coordinates'][0])-1):
                
                    within_range = impute_segment_range(gps,
                                                        temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                                        temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])
                    print(idx)

                    if within_range:
                    
                        p2s_distance = min_distance(gps, gps,
                                                    temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                                    temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])
                        print("point to segemint distance : ",p2s_distance)

                        heading = bearing(s_gps, gps,
                                          temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx],
                                          temp_segments[segments_index][segment_index]['geometry']['coordinates'][0][idx+1])
                        segment_index = temp_segment_index
                        segments_index = temp_segments_index
                        break
                s_number = 0

            # 유지
            if segment_range & (p2s_distance < p2s_value) & heading: # (heading 오류의 관한 처리 필요)
                print("유지")
                print("-----------------------------------------------------")
                s_gps = traj[gps_index] # s_gps을 현재 gps로 변환
                # 마지막 GPS 까지 확인 한 경우
                if gps_index == len(traj)-1:
                
                    end_segment_index = traj.index(s_gps)
                    segment_id = segments[segments_index][segment_index]['properties']['LINK_ID']
                    mapping[segment_id] = start_segment_index, end_segment_index


            
            # 링크 이동
            elif (not segment_range) & (p2s_distance < p2s_value):
                print("링크 이동")            
                segments.append(segment)
                segments_index = segments_index + 1
                segment_index = 0

                end_segment_index = traj.index(gps)-1
                segment_id = segments[segments_index-1][segment_index]['properties']['LINK_ID']
                mapping[segment_id] = start_segment_index, end_segment_index
                start_segment_index = end_segment_index+1 # start_segment_index을 현재 gps index로 변환
                
#                s_gps = pre_index # s_gps을 현재 gps로 변환
                s_gps = traj[gps_index]

            
            #링크 유실, 매핑 오류
            elif segment_range & (p2s_distance > p2s_value) | (not segment_range) & (p2s_distance > p2s_value) :
                print("링크 유실, 매핑 오류")
                # 매핑 오류 및 링크 유실로 확정날 때, 오류가 발견된 처음 GPS 위치
                if error_weight == 0:
                    weight_s_gps = traj.index(s_gps)

                # 가중치 값을 이용하여 매핑 오류 추정
                if error_weight == 1:
                    # find_segment를 하여 링크 유실인지, 매핑 오류인지 확인
#                    temp_segment = find_segment(gps)
                    temp_segment = -1
                        # 매핑 오류
                    if temp_segment == -1:
                        print("매핑 오류") 
                        # 처음으로 되돌아가서 작업 수행
                        #trajectory2segment(traj, segment_index=segment_index+1)
                        segment_index = segment_index+1
                        mapping = trajectory2segment(segment_index, segments)
                        break
                        
                        # 링크 유실
                    elif temp_segment == -1:
                        print("링크 유실")
                        end_segment_index = weight_s_gps-1
                        segment_id = segments[segments_index][segment_index]['properties']['LINK_ID']
                        mapping[segment_id] = start_segment_index, end_segment_index                  
                        break
                
                error_weight = error_weight + 1
            
            s_gps = gps

            # 잠깐의 오류로 임계값을 넘은경우를 위한 리셋 기능
            count = count + 1
            if count == 3:
            
                error_weight = 0

        else:
            print("범위안", gps_index )
    return mapping



def find_segment(gps):

    # GPS에 가장 가까운 세그먼트 k 개를 찾음
    # segments = {[link_id:{F_node, T_node, Lenth, geometry:[gps1, ... gpsn]}, ... ]}
    # return segments, -1
    pass


def impute_segment_range(gps, segment_s_gps, segment_e_gps):

    # paul Bourke의 Minimum Distance between a Point and a Line의 세그먼트와 점이 직교하는 위치에 있는지 확인해주는 공식 이용
    # gps가 segment의 양 끝 점을 기준으로 포함되었는지 확인
    # return True or False

    x1 = segment_s_gps[1]
    y1 = segment_s_gps[0]
    x2 = segment_e_gps[1]
    y2 = segment_e_gps[0]
    x3 = gps[0] # 데이터 형태에 따라 바꿔줘야함
    y3 = gps[1]

    result = False

    value = ((x3-x1)*(x2-x1)+(y3-y1)*(y2-y1))/((x2-x1)**2+(y2-y1)**2)
    print("range : ",value)

#    if (value > 0) & (value <= 1):
    if value <= 1:
        result = True
    else:
        result = False
    return result

def min_distance(s_gps, e_gps=[], s_segment=[], e_segment=[]):

    # 2개의 GPS의 거리를 계산 or GPS와 segment의 거리를 계산
    # return int
    value = 0
    if len(s_segment) > 0:
        x, y = point_in_seg(s_segment[1], s_segment[0], e_segment[1], e_segment[0], s_gps[0], s_gps[1])
        pre_point = (x, y)
        point = (s_gps[0], s_gps[1])
        value = haversine(pre_point, point, unit='m')
    else:
        pre_point = (s_gps[0], s_gps[1])
        point = (e_gps[0], e_gps[1])
        value = haversine(pre_point, point, unit='m')
    return value

def point_in_seg(x1, y1, x2, y2, x3, y3):

    '''
    함수 개요 : segment와 궤적의 직교하는 점을 구하기 위한 함수
    매개 변수 : x1, y1 = s_segment GPS
                x2, y2 = e_segment GPS
                x3, y3 = trajectory GPS
    함수 결과 : segment내에서 궤적의 GPS와 직교하는 위치 정보(위도, 경도)
    '''

    f_a = ((y2-y1)/(x2-x1))
    f_b = ((y2-y1)/(x2-x1))*-x1+y1
    
    a = -f_a**-1
    b = f_a**-1*x3+y3

    x = (b-f_b)/(f_a-a)
    y = a*x+b
    return x, y

def bearing(s_gps, e_gps, seg_point1, seg_point2):

    # 두 GPS의 heading value와 segment heading value를 비교하여 유사하면 True, 아니면 Flase
    # return True or False
    gps_heading = bearing_calculation(s_gps[0], s_gps[1], e_gps[0], e_gps[1])
    seg_heading = bearing_calculation(seg_point1[1], seg_point1[0], seg_point2[1], seg_point2[0])
    print("gps heading",gps_heading,"seg_heading", seg_heading)
    if abs(gps_heading - seg_heading) < 45:
        return True
    else:
        return False

def bearing_calculation(s_lat, s_lng, e_lat, e_lng):
    lat1 = radians(s_lat)
    lat2 = radians(e_lat)
    diffLong = radians(e_lng - s_lng)

    b_x = sin(diffLong) * cos(lat2)
    b_y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))
    initial_bearing = atan2(b_x, b_y)
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360 
    return int(compass_bearing)


def next_segments(segments, gps, gps_index, count):

    # segment의 F_node, T_node를 통해서 연결되는 segment를 찾고,
    # gps = traj[gps_index]부터 min_distance(gps, next_gps)을 계산해 임계값을 벗어나는 포인트 2개를 찾고,
    # 포인트 2개와 가장 가까운 segment를 리턴
    # segments = {[link_id:{F_node, T_node, Lenth, geometry:[gps1, ... gpsn]}, ... ]}
    # return segments, index, pre_index (수정필요 : gps_index or error(ex -1) 다음 gps계산을 미리 하기 때문에 - 재귀함수로 해결 할 예정)
    pass


# 추가 사항
# 모든 링크는 연결 되어 있으므로 다음 세그먼트가 없는 경우는 없다.


mapping = trajectory2segment()
print(mapping)
