import requests
from bs4 import BeautifulSoup
import sys
import os


path = "C:\\Users\\Shawn\\hafsautoleave\\hafsautoleave" #Project path
if path not in sys.path:
    sys.path.append(path) #Add to python import search path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hafsautoleave.settings") #Add environment variable

import django

django.setup()

#Django Setup Completed

from .models import GoingInfo

login_data = {
    'login_gubun' : 'student',
    'student_no' : '30228',
    'image.x' : '0',
    'image.y' : '0',
    'student_pw' : '30228'
}

with requests.Session() as s:
    
    # 로그인 URL
    url = "http://going.hafs.hs.kr/login/login_process.php"
    
    # Initiate login
    r = s.post(url, data = login_data)
    
    if ("alert" in str(r.content)):
        print("Wrong Login Data")
        raise Exception("Wrong Login Data")
    
    # Logged in
    r = s.get('http://going.hafs.hs.kr/lod/out_list_student_h.php')
    
    
    # 비정기 외출 신청 get request
    r = s.get("http://going.hafs.hs.kr/lod/out_reg2_student_h.php")
    r.encoding = 'euc-kr'
    
    # 외출 정보
    soup = BeautifulSoup(r.content, 'html5lib')
    student_seq = soup.find('input', attrs = {'name' : 'student_seq'})["value"]  # Find student sequence number
    
    out_date = "2019-07-31"
    out_hour = "22"
    out_minute = "00"
    return_date = "2019-07-31"
    return_hour = "23"
    return_minute = "00"
    
    leave_time_data = {
        "student_seq" : student_seq,
        "search_YN" : 'Y',
        "base_seq" : '',
        "out_date" : out_date,
        "out_hour" : out_hour,
        "out_minute" : out_minute,
        "return_date" : return_date,
        "return_hour" : return_hour,
        "return_minute" : return_minute,
        "bigo" : '',
        "count" : ''
    }
    
    r = s.post("http://going.hafs.hs.kr/lod/out_reg2_student.php", data = leave_time_data)
    r.encoding = 'euc-kr'
    print("Status:" , r.status_code)
    print(r.text)