# requests 와 json 을 활용하여 slack bot 조작하기
from time import sleep, strftime
import requests
import json
import os

import time
from datetime import datetime

# 메시지를 보내는 부분. 함수 안 argument 순서 :
# token : Slack Bot의 토큰
# channel : 메시지를 보낼 채널 #stock_notice
# text : Slack Bot 이 보낼 텍스트 메시지. 마크다운 형식이 지원된다.
# attachments : 첨부파일. 텍스트 이외에 이미지등을 첨부할 수 있다.
file_path = "./config/config.json"
data = []
#config 파일 읽기
print('####### Auto git push & Slack push bot start ######')
with open(file_path, 'r') as file:
    data = json.load(file)


def notice_message(token, channel, text, attachments):
    attachments = json.dumps(attachments) # 리스트는 Json 으로 덤핑 시켜야 Slack한테 제대로 간다.
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel, "text": text ,"attachments": attachments})

def handler_Slack_message(msg):

    time_title = datetime.now().strftime("%Y-%m-%d %H:%M")+' 깃 자동 업데이트를 사용합니다.'
    channel = msg['channel']
    send_text = msg['msg_text']
    stream = os.popen(msg['run_script'])
    output = stream.read()
    print(output)
    attach_dict = {
        'color' : msg['msg_color'],
        'author_name' : msg['msg_author'],
        'title' : time_title,
        'text' : output
    } # attachment 에 넣고싶은 목록들을 딕셔너리 형태로 입력
    attach_list=[attach_dict] # 딕셔너리 형태를 리스트로 변환
    notice_message(data["token"], channel, send_text, attach_list)

basicSleep = 60 * 40
 
# print(data['msg'][0]['rsv_time']) 

while(True):
    now = datetime.now()
    SleepCnt = 4
    while(SleepCnt > 0):
        flag = False
        for idx in range(len(data['msg'])):
            if(now.hour == data['msg'][idx]['rsv_time']):
                handler_Slack_message(data['msg'][idx])
        if(flag): 
            break
        print("Sleep 5 min from now on...")
        sleep(60*5)
        SleepCnt=SleepCnt-1
    s = str(round((basicSleep + SleepCnt*60*5)/60))
    print("Sleep "+ s +" min from now on...")
    print(basicSleep + SleepCnt*60*5)
    time.sleep(basicSleep + SleepCnt*60*5)
   
    