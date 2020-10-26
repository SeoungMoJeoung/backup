#-*- coding: utf-8 -*-

from haversine import haversine

# def trajectory2segment(traj, param_segment_index=0):

def trajectory2segment(param_segment_index=0):

    start_segment_index = 0 # 매핑할 세그먼트에 첫번재 포인트의 인덱스
    end_segment_index = 0 # 매핑할 세그먼트에 마지막 포인트의 인덱스
    error_weight = 0 # 매핑 추정 과정에서 반복적으로 오류가 발견될 때 확인하는 변수
    count = 0 # 매핑 추정 과정의 리셋을 위한 카운터
    gps_index = 0 # 현재 GPS 인덱스
    segment_index = param_segment_index # 궤적이 지나는 세그먼트들 중에서 GPS 한점과 가장 가까운 세그먼트를 찾기위한 인덱스
    segments_index = 0 # 궤적이 지나는 세그먼트들의 인덱스
    contiune_index = -1
    pre_index = 0

    mapping = {} # 매핑된 데이터
    segments = [] # 궤적이 지나는 세그먼트들
    segment = [] # 궤적이 지나는 세그먼트들 중에 하나의 segment

    traj=[[37.614588358484696,126.68074620792116],[37.61472433159179,126.68105143584104],[37.61480630659961,126.68137954785149],[37.61485205839804,126.68163985725627],[37.61470823850412,126.68176505933367],[37.61457367243557,126.68198083147205],[37.61441216822518,126.68223069613983],[37.61416939287934,126.68241294818185],[37.613953707406296,126.6826177361947],[37.613737960679536,126.68279987104285],[37.61350385940894,126.68285749583194],[37.61334214036464,126.68302807350976],[37.61328844684504,126.68316421402565],[37.61321712871292,126.68344766761399],[37.61318166675583,126.68366301259837],[37.61317311228891,126.68383293934181]]

    data = {'type': 'Feature', 'properties': {'LINK_ID': '1680083400', 'F_NODE': '1680033200', 'T_NODE': '1680021200', 'LANES_': 2.0, 'ROAD_RANK_': '106', 'ROAD_TYPE_': '000', 'ROAD_NO_': '0', 'ROAD_NAME_': '인천기타1길', 'ROAD_USE_': '0', 'MULTILINK': '0', 'CONNECT_': '000', 'MAX_SPD_': 30.0, 'REST_VEH_': '0', 'REST_W_': 0.0, 'REST_H_': 0.0, 'LENGTH': 477.871878453, 'REMARK_': '더미노드'}, 'geometry': {'type': 'MultiLineString', 'coordinates': [[[126.68016491977865, 37.61437499981774], [126.68123700013744, 37.614736979159126], [126.68140907979664, 37.61477900989836], [126.68153292048508, 37.6147799991889], [126.68166900063119, 37.61474904000363], [126.68236596090726, 37.61420201992182], [126.68244911936958, 37.61410895933151], [126.68250384048774, 37.61403201017427], [126.6827248794085, 37.61360100033895], [126.68286996051177, 37.613364029361954], [126.68297616014647, 37.61324297992764], [126.68315795982777, 37.613162969653146], [126.68391287981888, 37.61306496042543], [126.68437188033015, 37.61291996985817]]]}}

    segment.append(data)
    segments.append(segment)
#    print(type(segments[0][0]['geometry']['coordinates'][0][0]))
#    print(segments[0][0]['geometry']['coordinates'][0][0])

#    if param_segment_index == 0:

#        segment = find_segment(traj[gps_index])
#        segments.append(segment)
    
    s_gps = traj[gps_index] # 점과 점사이의 거리가 임계값을 넘어갔을 때, 이전 GPSㅡ
    p2s_distance = 999999999
    heading = False


    for gps in traj[1:]: # 수정 : index로 변경 해야함
    
        gps_index = traj.index(gps) # 현재 GPS index
        print("gps_index : ",gps_index)
        if gps_index < contiune_index:

            contiune
        
        p2p_distance = min_distance(s_gps, gps)
        print("p2p_distance: ",p2p_distance)
        p2p_value = 100
        if p2p_distance > p2p_value:  # GPS들의 거리를 먼저구해 임계값의 포함되면 아래와 같은 계산을 하지 않고 매핑
#            print(segments[segments_index][segment_index]['geometry']['coordinates'][0][0])
#            print(segments[segments_index][segment_index]['geometry']['coordinates'][0][-1])
#            print(gps)
            segment_range = impute_segment_range(gps,
                                                 segments[segments_index][segment_index]['geometry']['coordinates'][0][0],
                                                 segments[segments_index][segment_index]['geometry']['coordinates'][0][-1])
#            print(segment_range)
            '''
            if segment_range:
            
                for idx in range(len(segments[segments_index][segment_index][geometry])-1):
                
                    within_range = impute_segment_range(gps,
                                                        segments[segments_index][segment_index][geometry][idx],
                                                        segments[segments_index][segment_index][geometry][idx+1])
                    if within_range:
                    
                        p2s_distance = min_distance(gps,
                                                    segments[segments_index][segment_index][geometry][idx],
                                                    segments[segments_index][segment_index][geometry][idx+1])

                        heading = bearing(s_gps, e_gps = gps,
                                          segments[segments_index][segment_index][geometry][idx],
                                          segments[segments_index][segment_index][geometry][idx+1])
                        break
                    
            else:
            
                segment, contiune_index, pre_index = next_segments(segments[segments_index][segment_index][link_id], gps, gps_index, count) # 다음 새그먼트를 현재 새그먼트로 변환, count : 임계 값
                segments.append(segment)
                segments_index = segments_index + 1
                
                for idx in range(len(segments[segments_index][segment_index][geometry])-1):
                
                    within_range = impute_segment_range(gps,
                                                        segments[segments_index][segment_index][geometry][idx],
                                                        segments[segments_index][segment_index][geometry][idx+1])
                    if within_range:
                    
                        p2s_distance = min_distance(gps,
                                                    segments[segments_index][segment_index][idx],
                                                    segments[segments_index][segment_index][idx+1])
                        heading = bearing(s_gps, e_gps = gps,
                                          segments[segments_index][segment_index][idx],
                                          segments[segments_index][segment_index][idx+1])
                        break
            # 유지
            if sement_range & p2s_distance < p2s_value & heading: # (heading 오류의 관한 처리 필요)
            
                s_gps = traj[gps_index] # s_gps을 현재 gps로 변환
                # 마지막 GPS 까지 확인 한 경우
                if gps_index == len(traj):
                
                    end_segment_index = s_gps
                    segment_id = segments[segments_index][segment_index][link_id]
                    mapping[segment_id] = start_segment_index, end_segment_index
            
            # 링크 이동
            elif not segment_range & p2s_distance < p2s_value:
            
                end_segment_index = s_gps
                segment_id = segments[segments_index-1][segment_index][link_id]
                mapping[segment_id] = start_segment_index, end_segment_index
                start_segment_index = gps_index # start_segment_index을 현재 gps index로 변환
                
                s_gps = pre_index # s_gps을 현재 gps로 변환
            

            #링크 유실, 매핑 오류
            elif segment_range & p2s_distance > p2s_value:
            
                weight_s_gps = 0
                # 매핑 오류 및 링크 유실로 확정날 때, 오류가 발견된 처음 GPS 위치
                if error_weight == 0:
                
                    weight_s_gps = s_gps

                # 가중치 값을 이용하여 매핑 오류 추정
                if error_weight == 2:
                
                    # 범위 안  링크 유실, 매핑 오류
                    if segment_range & p2s_distance > p2s_value:
                    
                        # find_segment를 하여 링크 유실인지, 매핑 오류인지 확인
                        temp_segment = find_segment(gps)

                        # 매핑 오류
                        if temp_segment:
                        
                            # 처음으로 되돌아가서 작업 수행
                            mapping = trajectory2segment(traj, segment_index=segment_index+1)
                        
                        # 링크 유실
                        elif temp_segment == -1:
                        
                            end_segment_index = weight_s_gps
                            segment_id = segments[segments_index][segment_index][link_id]
                            mapping[segment_id] = start_segment_index, end_segment_index                  
                            break
                
                error_weight = error_weight + 1
            
            # 잠깐의 오류로 임계값을 넘은경우를 위한 리셋 기능
            count = count + 1
            if count == 3:
            
                error_weight = 0
            
    return mapping

'''

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

    if (value > 0) & (value <= 1):
        result = True
    else:
        result = False
    return result

def min_distance(gps1, gps2, segment1=[], segment2=[]):

    # 2개의 GPS의 거리를 계산 or GPS와 segment의 거리를 계산
    # return int
    test = haversine(gps1, gps2, unit='m')
    return test

def bearing(s_gps, e_gps, seg_point1, seg_point2):

    # 두 GPS의 heading value와 segment heading value를 비교하여 유사하면 True, 아니면 Flase
    # return True or False
    pass


def next_segments(segments, gps, gps_index, count):

    # segment의 F_node, T_node를 통해서 연결되는 segment를 찾고,
    # gps = traj[gps_index]부터 min_distance(gps, next_gps)을 계산해 임계값을 벗어나는 포인트 2개를 찾고,
    # 포인트 2개와 가장 가까운 segment를 리턴
    # segments = {[link_id:{F_node, T_node, Lenth, geometry:[gps1, ... gpsn]}, ... ]}
    # return segments, index, pre_index (수정필요 : gps_index or error(ex -1) 다음 gps계산을 미리 하기 때문에 - 재귀함수로 해결 할 예정)
    pass


# 추가 사항
# 모든 링크는 연결 되어 있으므로 다음 세그먼트가 없는 경우는 없다.


trajectory2segment()
