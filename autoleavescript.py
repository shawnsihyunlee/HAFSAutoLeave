import requests
from bs4 import BeautifulSoup
import sys
import os
import datetime
import re

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
saturday = friday + datetime.timedelta(days=1)
sunday = friday + datetime.timedelta(days=2)

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

        #Debug
        # print(f"Login Data for {info.user.username}:")
        # print(login_data)

        with requests.Session() as s:
            
            # 로그인 URL
            url = "http://going.hafs.hs.kr/login/login_process.php"
            try:
                # Initiate login
                r = s.post(url, data = login_data)
                
                if ("alert" in str(r.content)):
                    #print("Wrong Login Data")
                    raise Exception("Wrong Login Data")
                
                # Logged in
                #r = s.get('http://going.hafs.hs.kr/lod/out_list_student_h.php')
                
                
                # 정기 외출 신청 get request
                print("Getting student_seq...") #Debug
                r = s.get("http://going.hafs.hs.kr/lod/out_reg_student_h.php")
                r.encoding = 'euc-kr'
                
                # 외출 정보
                soup = BeautifulSoup(r.content, 'html.parser')
                student_seq = soup.find('input', attrs = {'name' : 'student_seq'})["value"]  # Find student sequence number
                print("Got student_seq : ", student_seq) #Debug

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

                initial_data = {
	                'student_seq': student_seq,
	                'search_YN': 'Y',
	                'base_seq': '',
	                'except': 'Y',
	                'out_date': out_date,
	                'out_hour': out_hour,
	                'out_minute': out_minute,
	                'return_date': return_date,
	                'return_hour': return_hour,
	                'return_minute': return_minute,
	                'count': '3',
                }

                # Get 식사 제외 times cuz I don't wanna do it via my own algorithm
                print("Getting 식사제외 times...")
                r = s.post("http://going.hafs.hs.kr/lod/out_reg_student_h.php", data = initial_data)
                r.encoding = 'euc-kr'

                soup = BeautifulSoup(r.content, 'html.parser')
                count = int(soup.find('input', attrs = {'name' : 'count'})["value"])
                chk = []
                for i in range(count):
                    chk.append(soup.find('input', attrs = {'name' : f'chk[{i+1}]'})["value"])
                print("Got 식사제외 times")
                #Sanity Check
                print("Sanity Check:")
                print(chk)

                #Final POST data
                leave_time_data = {
                'student_seq': student_seq,
                'search_YN': 'Y',
                'base_seq': '',
                'except': 'Y',
                'out_date': out_date,
                'out_hour': out_hour,
                'out_minute': out_minute,
                'return_date': return_date,
                'return_hour': return_hour,
                'return_minute': return_minute,
                "no_eat_chk": 'Y',
                "count": str(count),
                }

                for i in range(count):
                    leave_time_data[f'chk[{i+1}]'] = chk[i]


            	# <input type='hidden' checked name='chk[1]' value='2019-08-16|4'> <input type='hidden' checked name='chk[2]' value='2019-08-17|1'><input type='hidden' checked name='chk[3]' value='2019-08-17|2'> <input type='hidden' checked  name='chk[4]' value='2019-08-17|3'><input type='hidden' checked name='chk[5]' value='2019-08-17|4'> <input type='hidden' checked name='chk[6]' value='2019-08-18|1'> <input type='hidden' checked name='chk[7]' value='2019-08-18|2'> <input type='hidden' checked name='chk[8]' value='2019-08-18|3'> <input type='hidden' checked name='chk[9]' value='2019-08-18|4'>

            	# <input type="hidden" name="count" value="9">

                #print(leave_time_data) #debugging
                
                print("Doing final signup...")
                r = s.post("http://going.hafs.hs.kr/lod/aa.php", data = leave_time_data)
                r.encoding = 'euc-kr'
                #print("Status:" , r.status_code)
                print(r.text)
                # soup = BeautifulSoup(r.content, 'html.parser')
                # script = soup.find("script").extract()
                # # find all alert text
                # alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text)
                # print(alert)
            except Exception as e:
                print("ERROR:")
                print(e)
                print()

doSignup()