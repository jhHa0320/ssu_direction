# SSU Direction
숭실대학교 교내 길찾기 프로그램

## 사용된 언어 및 프레임워크
- **Python**
- **Django**
- **Folium**
- **OSMNX**
- **HTML/CSS/JavaScript**

## 프로젝트 설명
2024년 1학년 1학기 **프로그래밍 및 실습 1** 과목에서 진행한 개인 프로젝트 과제입니다. 

학교 캠퍼스 내부에서 **네이버 길찾기** 기능이 바람직한 길찾기 경로를 보여주지 않는 것을 발견하여, 숭실대학교만의 길찾기 프로그램을 만들고자 하였습니다. 

### 주요 기능
- **건물-건물 길찾기**: 캠퍼스 내 건물 간의 최적 경로를 제공합니다.
- **편의시설 시각화**: Folium을 이용해 캠퍼스 내 편의시설을 한눈에 볼 수 있는 기능을 추가했습니다.

> **참고**: 강의실 간 기능(ex. 진리관 1xx호 ~ 학생회관 2xx호)은 학교 건물 구조를 파악하는 작업이 쉽지 않아, 현재는 건물-건물 길찾기 기능만 구현한 상태입니다. 추후 개선할 예정입니다.

## 시연
![image](https://github.com/user-attachments/assets/91b5469d-57c9-4577-a807-aa8aaa4639fd)

![image](https://github.com/user-attachments/assets/ddb8fb83-26ec-4287-a269-042f6697cf1a)

![image](https://github.com/user-attachments/assets/a93fdfb4-e4bf-405d-b3ac-120db1a4c516)

![image](https://github.com/user-attachments/assets/c7f02c06-9969-40d5-8182-9c78f52c6c59)

![image](https://github.com/user-attachments/assets/7c04e052-136a-41e5-8f5e-e473b8ea3239)

![image](https://github.com/user-attachments/assets/28161ce7-7047-4df7-9884-55eb84dc1f03)


## 설치 방법
1. 저장소 클론:
   ```bash
   git clone https://github.com/username/ssu_direction.git
   cd ssu_direction
2. 가상환경 설정:    
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate     # Windows
3. django, folium, osmnx 설치
   pip install django
   pip install folium
   pip install osmnx
4. 서버 실행:
   python manage.py runserver
5. 브라우저에서 https://127.0.0.1:8000 또는 생성된 링크로 이동하여 확인합니다.
