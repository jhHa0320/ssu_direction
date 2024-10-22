from django.urls import path
from .views import home, calculate_route, building_info
from .views import gyoyuk, globalBrainHall, residenceHall, munhwa, mirae, baekma, baird, venture, gyeongsang, shinyang
from .views import ahniktae, yeongu, westerminster, jeonsan, jeongbo, chomansik, library, jinri, changsin, changui
from .views import studentCenter, hangyeongjik, churchMuseum, hyeongnam



urlpatterns = [
    path('', home, name='home'),
    path('calculate_route/', calculate_route, name='calculate_route'),
    path('교내_건물/', building_info, name='교내_건물'),
        
    path('교육관/', gyoyuk, name='교육관'),
    path('글로벌브레인홀/', globalBrainHall, name='글로벌브레인홀'),    
    path('레지던스홀/', residenceHall, name='레지던스홀'),
    path('문화관/', munhwa, name='문화관'),
    path('미래관/', mirae, name='미래관'),
    path('백마관/', baekma, name='백마관'),
    path('베어드홀/', baird, name='베어드홀'),
    path('벤처중소기업센터/', venture, name='벤처중소기업센터'),
    path('숭덕경상관/', gyeongsang, name='숭덕경상관'),
    path('신양관/', shinyang, name='신양관'),
    path('안익태기념관/', ahniktae, name='안익태기념관'),
    path('연구관/', yeongu, name='연구관'),
    path('웨스터민스터홀/', westerminster, name='웨스터민스터홀'),
    path('전산관/', jeonsan, name='전산관'),
    path('정보과학관/', jeongbo, name='정보과학관'),
    path('조만식기념관/', chomansik, name='조만식기념관'),
    path('중앙도서관/', library, name='중앙도서관'),
    path('진리관/', jinri, name='진리관'),
    path('창신관/', changsin, name='창신관'),
    path('창의관/', changui, name='창의관'),
    path('학생회관/', studentCenter, name='학생회관'),
    path('한경직기념관/', hangyeongjik, name='한경직기념관'),
    path('한국기독교박물관/', churchMuseum, name='한국기독교박물관'),
    path('형남공학관/', hyeongnam, name='형남공학관'),
]

