from django.shortcuts import render, redirect
import folium as flm
import osmnx as ox
import networkx as nx
from django.views.decorators.csrf import csrf_exempt
from folium import plugins

ox.config(log_console=True, use_cache=True)

# 장소 정보를 모아둘 클래스 선언
# 건물과 지하철역 클래스 상속
class Spot:
    def __init__(self, location, name, address):
        self.location = location
        self.name = name
        self.address = address

class Building(Spot):
    def __init__(self, location, name, address, rooms):
        super().__init__(location, name, address)
        self.rooms = rooms

class Station(Spot):
    def __init__(self, location, name, address):
        super().__init__(location, name, address)

# 대분류 카테고리 요소
mainCategory = [
    '건물',
    '숭실대입구역',
]

# 레지던스홀 카테고리 목록(예시)
residenceHall_list_floor = ['지하 1층']
temp = [f'지상 {i}층' for i in range(1, 13)]
residenceHall_list_floor.extend(temp)
residenceHall_list = ['기숙사식당', '편의점', '체력단련실']
temp = [f'{i}호' for i in range(101, 118)]
residenceHall_list.extend(temp)
temp = [f'{i}호' for i in range(151, 169)]
residenceHall_list.extend(temp)
temp = [f'{i}호' for i in range(201, 274)]
residenceHall_list.extend(temp)

# 건물 인스턴스
# 구글맵에서 좌표 정보 가져옴
# 레지던스홀 이외의 건물에는 호수를 101호 1개만 일단 입력해둠
buildings = [
    Building([37.4977651, 126.9568346], '교육관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4956817, 126.9604895], '글로벌브레인홀', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4950731, 126.9603531], '레지던스홀', '서울 동작구 상도로 369', [f'{residenceHall_list}']),
    Building([37.4964596, 126.9543349], '문화관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4956025, 126.9584825], '미래관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4977928, 126.956168], '백마관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4964596, 126.956307], '베어드홀', '서울 동작구 상도로 369', ['101호',]),
    Building([37.497544, 126.957455], '벤처중소기업센터', '서울 동작구 상도로 369', ['101호'] ),
    Building([37.4964874, 126.9551682], '숭덕경상관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4960259, 126.9581436], '신양관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4957097, 126.9550571], '안익태기념관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4962653, 126.9591956], '연구관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4968208, 126.958529], '웨스터민스터홀', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4954321, 126.9596122], '전산관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4945268, 126.9598527], '정보과학관', '서울 동작구 사당로 50', ['101호',]),
    Building([37.4971263, 126.9584178], '조만식기념관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4962097, 126.9585845], '중앙도서관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.496968, 126.957339], '진리관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4946403, 126.9594151], '창신관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4946403, 126.9594151], '창의관', '서울 동작구 사당로 46', ['101호',]),
    Building([37.496797, 126.956593], '학생회관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4955709, 126.9575846], '한경직기념관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4955153, 126.9570569], '한국기독교박물관', '서울 동작구 상도로 369', ['101호',]),
    Building([37.4957653, 126.9561681], '형남공학관', '서울 동작구 상도로 369', ['101호',]),
]

stations = [
    Station([37.495054, 126.954415], '1번 출구', '서울 동작구 상도로 378'),
    Station([37.495633, 126.953894], '2번 출구', '서울 동작구 상도로 378'),
    Station([37.495923, 126.954224], '3번 출구', '서울 동작구 상도로 378'),
    Station([37.495322, 126.954746], '4번 출구', '서울 동작구 상도로 378'),
]

spots = buildings + stations

# home 화면(첫 화면 세팅)
def home(request):
    # folium을 통한 숭실대 부근 지도 불러옴(ssuMap)
    ssuMap = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=18,
        tiles="OpenStreetMap"
    )
    
    # 건물 그룹(마커)
    building_group = flm.FeatureGroup("건물").add_to(ssuMap)
    for building in buildings:
        url = f"{building.name}/" 
        popup_html = f'<a href="{url}" target="_blank">건물 내부 보기(이동 경로 탐색)</a>'
        
        flm.Marker(
            location=building.location,
            tooltip=f"<b>{building.name}</b><br>{building.address}",
            popup = flm.Popup(popup_html, max_width=300)
        ).add_to(building_group)
    
    # 숭실대입구역 출구 그룹(마커)
    station_group = flm.FeatureGroup("숭실대입구역(7호선)").add_to(ssuMap)
    for station in stations:
        flm.Marker(
            location=station.location,
            tooltip=f"<b>{station.name}</b><br>{station.address}",
            icon = flm.Icon(color='purple')
        ).add_to(station_group)
        
    # 그룹 선택 체크박스
    flm.LayerControl(collapsed=False).add_to(ssuMap)
    
    # 사용자 현위치
    plugins.LocateControl().add_to(ssuMap)
            

    # Folium 지도를 HTML 형식으로 변환(home.html 화면에 나타내기 위함)
    folium_map_html = ssuMap._repr_html_()

    # home.html로 보낼 정보
    context = {
        'folium_map_html': folium_map_html,
        'buildings': buildings,
        'stations' : stations,
        'mainCategory' : mainCategory,
        'spots' : spots,
    }
    return render(request, 'home.html', context)

# 경로 계산 처리 함수
# csrf라는 보안 공격을 막기 위한 데코레이터
@csrf_exempt
def calculate_route(request):
    if request.method == 'POST':
        # 중분류(건물 이름)으로 출발지와 목적지를 가져옴
        start_location = request.POST.get('start_location_sub')
        end_location = request.POST.get('end_location_sub')
        
        # 각 건물 좌표 매칭
        location_dict = {spot.name: spot.location for spot in spots}
        
        # OpenStreetMap 데이터를 사용하여 도보 네트워크 생성
        graph = ox.graph_from_place('Soongsil University, Seoul, South Korea', network_type='walk')
        
        # 각 빌딩의 노드 찾기
        start_coords = location_dict[start_location]
        end_coords = location_dict[end_location]
        
        # 입력된 좌표를 이용해 가장 가까운 노드 찾기
        start_node = ox.distance.nearest_nodes(graph, X=start_coords[1], Y=start_coords[0])
        end_node = ox.distance.nearest_nodes(graph, X=end_coords[1], Y=end_coords[0])
        

        try:
            # 최단 경로 계산 (커스텀 가중치 사용)
            path = nx.shortest_path(graph, start_node, end_node, weight=2.5)
            path_length = nx.shortest_path_length(graph, start_node, end_node, weight=2.5)

            # Folium을 사용하여 경로 플롯하기
            ssuMap = flm.Map(location=[37.4963538, 126.9572222], zoom_start=18, tiles="OpenStreetMap")

            # 경로의 좌표 리스트 생성
            route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]

            # 경로를 Folium PolyLine으로 추가
            flm.PolyLine(route_coords, color='blue', weight=2.5, opacity=1).add_to(ssuMap)
            
            # 출발지, 목적지 마커를 만들기 위해 건물 정보를 가져옴
            for spot in spots:
                if spot.name == start_location:
                    start_name = spot.name
                    start_loc = spot.location
                if spot.name == end_location:
                    end_name = spot.name
                    end_loc = spot.location    
            
            # 출발지 마커
            # 출발지 마커에 들어갈 텍스트 내용
            icon_html_start = f"""
            <div style='text-align: center; background-color: green; border-radius: 50px; padding: 5px; box-shadow: 2px 2px 5px grey;'>
                <div style='font-size: 18px; color: white'><b>출발지</b></div>
                <div style='font-size: 15px; color: white'>{start_name}</div>
            </div>
            """

            # 커스텀 DivIcon 생성(출발지)
            custom_icon_start = flm.DivIcon(
                icon_size=(150, 36),
                html=icon_html_start
            )
            popup_html_start = f'<a href="../{start_name}" target="_blank">건물 내부 보기/이동 경로 탐색</a>'
            
            # 커스텀 DivIcon을 사용하는 마커 생성(출발지)
            flm.Marker(
                location=start_loc,
                icon=custom_icon_start,
                popup=flm.Popup(popup_html_start, max_width=300)
            ).add_to(ssuMap)

            # 목적지 마커
            # 목적지 마커에 들어갈 내용
            icon_html_end = f"""
            <div style='text-align: center; background-color: red; border-radius: 50px; padding: 5px; box-shadow: 2px 2px 5px grey;'>
                <div style='font-size: 18px; color: white'><b>목적지</b></div>
                <div style='font-size: 15px; color: white'>{end_name}</div>
            </div>
            """

            # 커스텀 DivIcon 생성(목적지)
            custom_icon_end = flm.DivIcon(
                icon_size=(150, 36),
                html=icon_html_end
            )
            popup_html_end = f'<a href="../{end_name}" target="_blank">건물 내부 보기/이동 경로 탐색</a>'
            
            # 커스텀 DivIcon을 사용하는 마커 생성(목적지)
            flm.Marker(
                location=end_loc,
                icon=custom_icon_end,
                popup=flm.Popup(popup_html_end, max_width=300)
            ).add_to(ssuMap)            
        
            # Folium 지도를 HTML 형식으로 변환
            folium_map_html = ssuMap._repr_html_()
        
        # 최단 경로가 없다면 아무것도 반환하지 않음
        except nx.NetworkXNoPath:
            path = None
            folium_map_html = None

        context = {
            'path': path,
            'folium_map_html': folium_map_html,
        }
        return render(request, 'home.html', context)
    else:
        return redirect('home')

# 건물별로 함수를 선언해둠
def gyoyuk(request):
    
    return render(request, 'soon.html')

def globalBrainHall(request):
    
    return render(request, 'soon.html')

# 레지던스홀 정보 데이터를 resdienceHall.html로 보냄
def residenceHall(request):
    context ={
        'residenceHall_list' : residenceHall_list,
        'residenceHall_list_floor' : residenceHall_list_floor
    }
    return render(request, 'residenceHall.html', context)

def mirae(request):
    
    return render(request, 'soon.html')

def baekma(request):
    
    return render(request, 'soon.html')

def baird(request):
    
    return render(request, 'soon.html')

def venture(request):
    
    return render(request, 'soon.html')

def gyeongsang(request):
    
    return render(request, 'soon.html')

def ahniktae(request):
    
    return render(request, 'soon.html')

def shinyang(request):
    
    return render(request, 'soon.html')

def yeongu(request):
    
    return render(request, 'soon.html')

def westerminster(request):
    
    return render(request, 'soon.html')

def jeonsan(request):
    
    return render(request, 'soon.html')

def jeongbo(request):
    
    return render(request, 'soon.html')

def chomansik(request):
    
    return render(request, 'soon.html')

def library(request):
    
    return render(request, 'soon.html')

def jinri(request):
    
    return render(request, 'soon.html')

def changsin(request):
    
    return render(request, 'soon.html')

def changui(request):
    
    return render(request, 'soon.html')

def studentCenter(request):
    
    return render(request, 'soon.html')

def churchMuseum(request):
    
    return render(request, 'soon.html')

def hangyeongjik(request):
    
    return render(request, 'soon.html')

def munhwa(request):
    
    return render(request, 'munhwa.html')

def hyeongnam(request):
    
    return render(request, 'hyeongnam.html')

# 교내의 모든 건물 정보를 보여주는 페이지
def building_info(request):
    # 교내 식당을 보여주기 위한 지도(ssuMapRes)
    ssuMapRes = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=17.4,
        tiles="OpenStreetMap"
    )
    # 교내 식당, 카페, 편의점 위치 정보 불러옴
    for building in buildings:
        if building.name == '학생회관':
            studentCenterCafeterias = building
            studentCenterConv = building
        elif building.name == '신양관':
            dodam = building
            shinyangConv = building
            bankAndPost = building
        elif building.name == '전산관':
            jeonsanCafeterias = building
            jeonsanConv = building
            jeonsanATM = building
        elif building.name == '중앙도서관':
            libraryCafe = building
        elif building.name == '숭덕경상관':
            gyeongsangCafe = building
            gyeongsangConv = building
        elif building.name == '조만식기념관':
            chomansikCafe = building
            chomansikConv = building
            chomansikATM = building
        elif building.name == '웨스터민스터홀':
            westerminsterCafe = building
        elif building.name == '형남공학관':
            hyeongnamConv = building
            hyeongnamATM = building
        elif building.name == '레지던스홀':
            logInConv = building
        elif building.name == '베어드홀':
            bairdATM = building
        elif building.name == '정보과학관':
            jeongboATM = building
    
    # 식당 마커
    flm.Marker(
        location=studentCenterCafeterias.location,
        tooltip=f"<b>학생회관</b><br><b>학생식당(3층, 5,000)</b><br><b>스넥코너(3층)</b><br><b>푸드코드(2층)</b>",
        icon = flm.Icon(color='red'),
        icon_size=(150, 36)
    ).add_to(ssuMapRes)
    
    flm.Marker(
        location=dodam.location,
        tooltip=f"<b>신양관</b><br><b>도담식당(2층, 6,000)</b>",
        icon = flm.Icon(color='red'),
        icon_size=(150, 36)
    ).add_to(ssuMapRes)
    
    flm.Marker(
        location=jeonsanCafeterias.location,
        tooltip=f"<b>전산관</b><br><b>카페테리아(1층)</b><br><b>교수 식당(1층)</b>",
        icon = flm.Icon(color='red'),
        icon_size=(150, 36)
    ).add_to(ssuMapRes)
    
    folium_ssuMapRes_html = ssuMapRes._repr_html_()
    
    # 교내 카페를 보여주기 위한 지도(ssuMapCafe)
    ssuMapCafe = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=17.4,
        tiles="OpenStreetMap"
    )
    # 교내 카페 마커
    flm.Marker(
        location=gyeongsangCafe.location,
        tooltip=f"<b>숭덕경상관</b><br><b>달콤슈(2층, 가격)</b>",
        icon = flm.Icon(color='green'),
        icon_size=(150, 36)
    ).add_to(ssuMapCafe)
    
    flm.Marker(
        location=chomansikCafe.location,
        tooltip=f"<b>조만식기념관</b><br><b>커피앤티스토리(1층, 가격)</b>",
        icon = flm.Icon(color='green'),
        icon_size=(150, 36)
    ).add_to(ssuMapCafe)
    
    flm.Marker(
        location=westerminsterCafe.location,
        tooltip=f"<b>웨스터민스터홀</b><br><b>카페 331(3층, 가격)</b><br><b>푸드트럭 니키즈(3층 입구 뒤, 가격)</b>",
        icon = flm.Icon(color='green'),
        icon_size=(150, 36)
    ).add_to(ssuMapCafe)
    
    flm.Marker(
        location=libraryCafe.location,
        tooltip=f"<b>중앙도서관</b><br><b>숭실마루 커피점(6층, 가격)</b>",
        icon = flm.Icon(color='green'),
        icon_size=(150, 36)
    ).add_to(ssuMapCafe)
    
    # Folium 지도를 HTML 형식으로 변환
    folium_ssuMapCafe_html = ssuMapCafe._repr_html_()
   
    # 교내 편의점을 보여주기 위한 지도(ssuMapConv)
    ssuMapConv = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=17.4,
        tiles="OpenStreetMap"
    )
    
    # 교내 편의점 마커
    flm.Marker(
        location=hyeongnamConv.location,
        tooltip=f"<b>형남공학관</b><br><b>이마트24 형남공학관점(2층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)

    flm.Marker(
        location=studentCenterConv.location,
        tooltip=f"<b>학생회관</b><br><b>이마트24 숭실대학생회관점(4층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)
    
    flm.Marker(
        location=chomansikConv.location,
        tooltip=f"<b>조만식기념관</b><br><b>이마트24 숭실대조만식기념관점(2층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)
    
    flm.Marker(
        location=gyeongsangConv.location,
        tooltip=f"<b>숭덕경상관</b><br><b>이마트24 숭덕경상관(1층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)

    flm.Marker(
        location=jeonsanConv.location,
        tooltip=f"<b>전산관</b><br><b>이마트24 전산관(1층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)    

    flm.Marker(
        location=shinyangConv.location,
        tooltip=f"<b>신양관</b><br><b>이마트24 신양관(1층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)
    
    flm.Marker(
        location=logInConv.location,
        tooltip=f"<b>레지던스홀</b><br><b>LOG-IN 편의점(지하 1층)</b>",
        icon = flm.Icon(color='orange'),
        icon_size=(150, 36)
    ).add_to(ssuMapConv)
    
    # Folium 지도를 HTML 형식으로 변환
    folium_ssuMapConv_html = ssuMapConv._repr_html_()
   
    # 교내 은행과 우체국을 보여주기 위한 지도(ssuMapBankAndPost)
    ssuMapBankAndPost = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=17.4,
        tiles="OpenStreetMap"
    )
    
    # 교내 은행과 우체국 마커
    flm.Marker(
        location=bankAndPost.location,
        tooltip=f"<b>신양관</b><br><b>우체국, 우리은행(지하 1층)</b>",
        icon = flm.Icon(color='purple'),
        icon_size=(150, 36)
    ).add_to(ssuMapBankAndPost)
    
    folium_ssuMapBankAndPost_html = ssuMapBankAndPost._repr_html_()
    
    # 교내 ATM 위치를 보여주기 위한 지도(ssuMapATM)
    ssuMapATM = flm.Map(
        location=[37.4963538, 126.9572222], 
        zoom_start=17.4,
        tiles="OpenStreetMap"
    )
    # 교내 ATM 마커
    flm.Marker(
        location=hyeongnamATM.location,
        tooltip=f"<b>형남공학관</b><br><b>우리은행ATM(2층)</b>",
        icon = flm.Icon(color='blue'),
        icon_size=(150, 36)
    ).add_to(ssuMapATM)
    
    flm.Marker(
        location=bairdATM.location,
        tooltip=f"<b>베어드홀</b><br><b>우리은행, 국민은행ATM(2층)</b>",
        icon = flm.Icon(color='blue'),
        icon_size=(150, 36)
    ).add_to(ssuMapATM)
    
    flm.Marker(
        location=jeongboATM.location,
        tooltip=f"<b>정보과학관</b><br><b>우리은행ATM(1층)</b>",
        icon = flm.Icon(color='blue'),
        icon_size=(150, 36)
    ).add_to(ssuMapATM)
    
    flm.Marker(
        location=jeonsanATM.location,
        tooltip=f"<b>전산관</b><br><b>우리은행ATM(1층)</b>",
        icon = flm.Icon(color='blue'),
        icon_size=(150, 36)
    ).add_to(ssuMapATM)
    
    flm.Marker(
        location=chomansikATM.location,
        tooltip=f"<b>조만식기념관</b><br><b>우리은행, 신한은행ATM(1층)</b>",
        icon = flm.Icon(color='blue'),
        icon_size=(150, 36)
    ).add_to(ssuMapATM)
    
    # Folium 지도를 HTML 형식으로 변환
    folium_ssuMapATM_html = ssuMapATM._repr_html_()
   
    # 변환한 html 형식 folium 지도를 building_info로 전달
    context={
        'folium_ssuMapRes_html': folium_ssuMapRes_html,
        'folium_ssuMapCafe_html': folium_ssuMapCafe_html,
        'folium_ssuMapConv_html': folium_ssuMapConv_html,
        'folium_ssuMapBankAndPost_html' : folium_ssuMapBankAndPost_html,
        'folium_ssuMapATM_html' : folium_ssuMapATM_html,
        
    }
    return render(request, 'building_info.html', context)
