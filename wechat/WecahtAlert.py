#encoding:utf-8
import json
import requests
from elastalert.alerts import Alerter, BasicMatchString
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WechatAlerter(Alerter):

    cid = ""
    secret = ""
    to_tag = ""
    agent_id = ""
    # Alert is called
    def alert(self, matches):

        index_name = self.rule["index"]
        index_name_without_symbol = index_name.replace('-*', '')

        for match in matches:
            print("match",match)
            message = match.get("message")
            loglevel = match.get("logLevel")
            node = match.get("node","")
            self.push_weixin(index_name_without_symbol,loglevel,node,message)



    def push_weixin(self, index,loglevel,node,message):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.cid,self.secret)

        resp = requests.get(url)

        json_resp = resp.json()

        if json_resp.get("errmsg") != 'ok':
            return "weixin login fail"

        access_token = json_resp.get("access_token")

        msg_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (access_token)


        wxs = {
            "totag" : to_tag,
            "msgtype": "text",
            "agentid" : agent_id,
            "text": {
                    "content": "======start======\nES索引: %s\n日志级别: %s\n告警主机: %s\n告警内容: %s\n======end======\n" % (index,loglevel,node,message)
                }
            }


        r = requests.post(msg_url,json=wxs)

        if r.status_code != 200:
            print(r.text)
            return
