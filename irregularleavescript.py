import requests
from bs4 import BeautifulSoup
import sys
import os
import datetime

path = "C:\\Users\\Shawn\\hafsautoleave" #Project path
if path not in sys.path:
    sys.path.append(path) #Add to python import search path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hafsautoleave.settings") #Add environment variable

import django

django.setup()

#Django Setup Completed

from main.models import GoingInfo

# Calculate dates for this week
today = datetime.date.today()
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )
saturday = today + datetime.timedelta( (5-today.weekday()) % 7 )
sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )

#Convert to strings
friday = friday.strftime('%Y-%m-%d')
saturday = saturday.strftime('%Y-%m-%d')
sunday = sunday.strftime('%Y-%m-%d')

datedict = {'friday' : friday, 'saturday' : saturday, 'sunday' : sunday}

def doSignup():
    for info in GoingInfo.objects.filter(do_auto_signup = True):

        print(f"Initiating process for {info.user.username}")


        login_data = {
            'login_gubun' : 'student',
            'student_no' : info.student_id,
            'image.x' : '0',
            'image.y' : '0',
            'student_pw' : info.student_pass,
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
            soup = BeautifulSoup(r.content, 'html.parser')
            student_seq = soup.find('input', attrs = {'name' : 'student_seq'})["value"]  # Find student sequence number
            
            out_date = datedict[info.out_day.lower()]
            out_hour = str(info.out_hour)
            out_minute = str(info.out_minute)
            return_date = datedict[info.return_day.lower()]
            return_hour = str(info.return_hour)
            return_minute = str(info.return_minute)
            
            if(out_minute == "0"):
                out_minute = "00"
            if(return_minute == "0"):
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

            #print(leave_time_data) #debugging
            
            r = s.post("http://going.hafs.hs.kr/lod/out_reg2_student.php", data = leave_time_data)
            r.encoding = 'euc-kr'
            print("Status:" , r.status_code)
            print(r.text)
