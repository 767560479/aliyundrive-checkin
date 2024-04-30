import os
import re
import argparse
from aliyundrive import Aliyundrive
from message_send import MessageSend
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_string', type=str, required=True)
    args = parser.parse_args()

    token_string = args.token_string
    pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
    serverChan_sendkey = os.environ.get('SERVERCHAN_SENDKEY')
    weCom_tokens = os.environ.get('WECOM_TOKENS')
    weCom_webhook = os.environ.get('WECOM_WEBHOOK')
    bark_deviceKey = os.environ.get('BARK_DEVICEKEY')
    feishu_deviceKey = os.environ.get('FEISHU_DEVICEKEY')

    message_tokens = {
        'pushplus_token': pushplus_token,
        'serverChan_token': serverChan_sendkey,
        'weCom_tokens': weCom_tokens,
        'weCom_webhook': weCom_webhook,
        'bark_deviceKey': bark_deviceKey,
        'feishu_deviceKey': feishu_deviceKey,
    }

    token_string = token_string.split(',')
    ali = Aliyundrive()
    message_all = []

    for idx, token in enumerate(token_string):
        result = ali.aliyundrive_check_in(token)
        print(result)
        message_all.append(str(result))

        if idx < len(token_string) - 1:
            message_all.append('--')

    title = '阿里云盘签到结果'
    message_all = '\n'.join(message_all)
    message_all = re.sub('\n+', '\n', message_all).rstrip('\n')

    message_send = MessageSend()
    message_send.send_all(message_tokens, title, message_all)

    print('finish')


def definesys():
    url = "https://edu.definesys.cn/edu-api/forumSign/sign"
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE3MTUzNDg4MzYsImlhdCI6MTcxMjc1NjgzNiwieGRhcHVzZXJpZCI6IjEwMDM5MzA3MTE2MjgxNDM2NTY5NiJ9.YAhyUT-N1VMKsPqpMwlZaMrPCslPb8T0-HLbwv5sQWLYKFeZ40ycoA1ox9h3c5kS5LBOOnl4bXmmyGUbgJYS7g'
    # 请求头 添加token
    headers = {
      'token': f'{token}'
    }
    
    print('开始请求')
    response = requests.request("GET", url, headers=headers)
    print(response)

   # 检查响应状态码
    if response.status_code == 200:

        print('请求成功！')
        # 处理响应数据
        data = response.json()
        print(data)
    else:
        print('请求失败，状态码：', response.status_code)
    



if __name__ == '__main__':
    main()
    definesys()
