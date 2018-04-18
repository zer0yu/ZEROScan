#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import sys
import sqlite3
from lib.core.common import paths
from modules.useragent import *
from bs4 import BeautifulSoup
from thirdparty import requests
from thirdparty.requests.packages.urllib3.exceptions import InsecureRequestWarning

def expInfo():
    expInfo={}
    expInfo["appName"] = "CHECK CSM"
    expInfo["appVersion"] = "every version"
    expInfo["author"] = "Z3r0yu"
    expInfo["description"] = "To find what the web is"
    expInfo["references"] = "https://github.com/se55i0n/Webfinger"

    expInfo["options"] = [
        {
            "Name": "URL",
            "Current Setting": "",
            "Required": True,
            "Description": "URL or URL file"
        },
        {
            "Name": "Thread",
            "Current Setting": "1",
            "Required": False,
            "Description": "Threads"
        },
        {
            "Name": "Cookie",
            "Current Setting": "",
            "Required": False,
            "Description": "cookie"
        },
        {
            "Name": "Report",
            "Current Setting": "",
            "Required": False,
            "Description": "do you need a html report?"
        },
    ]
    return expInfo


#User-Agent
ua = get_random_agent()
agent = {'UserAgent':ua}

#re
rtitle   = re.compile(r'title="(.*)"')
rheader  = re.compile(r'header="(.*)"')
rbody    = re.compile(r'body="(.*)"')
rbracket = re.compile(r'\((.*)\)')

#中文乱码及ssl错误
def setting():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def check(_id):
	with sqlite3.connect(paths.WEB_DB) as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT name, keys FROM `fofa` WHERE id=\'{}\''.format(_id))
		for row in result:
			return row[0], row[1]

def count():
	with sqlite3.connect(paths.WEB_DB) as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT COUNT(id) FROM `fofa`')
		for row in result:
			return row[0]


class CMSScanner(object):
	def __init__(self, target):
		self.target = target
		self.result = ""
		setting()

	def get_info(self):
		"""获取web的信息"""
		try:
			r = requests.get(url=self.target, headers=agent,
				timeout=3, verify=False)
			content = r.text
			try:
				title = BeautifulSoup(content, 'lxml').title.text.strip()
				return str(r.headers), content, title.strip('\n')
			except:
				return str(r.headers), content, ''
		except Exception as e:
			pass

	def check_rule(self, key, header, body, title):
		"""指纹识别"""
		try:
			if 'title="' in key:
				if re.findall(rtitle, key)[0].lower() in title.lower():
					return True
			elif 'body="' in key:
				if re.findall(rbody, key)[0] in body:return True
			else:
				if re.findall(rheader, key)[0] in header:return True
		except Exception as e:
			pass

	def handle(self, _id, header, body, title):
		"""取出数据库的key进行匹配"""
		name, key = check(_id)
		#满足一个条件即可的情况
		if '||' in key and '&&' not in key and '(' not in key:
			for rule in key.split('||'):
				if self.check_rule(rule, header, body, title):
					return name
					break
		#只有一个条件的情况
		elif '||' not in key and '&&' not in key and '(' not in key:
			if self.check_rule(key, header, body, title):
				return name
		#需要同时满足条件的情况
		elif '&&' in key and '||' not in key and '(' not in key:
			num = 0
			for rule in key.split('&&'):
				if self.check_rule(rule, header, body, title):
					num += 1
			if num == len(key.split('&&')):
				return name
		else:
			#与条件下存在并条件: 1||2||(3&&4)
			if '&&' in re.findall(rbracket, key)[0]:
				for rule in key.split('||'):
					if '&&' in rule:
						num = 0
						for _rule in rule.split('&&'):
							if self.check_rule(_rule, header, body, title):
								num += 1
						if num == len(rule.split('&&')):
							return name
							break
					else:
						if self.check_rule(rule, header, body, title):
							return name
							break
			else:
				#并条件下存在与条件： 1&&2&&(3||4)
				for rule in key.split('&&'):
					num = 0
					if '||' in rule:
						for _rule in rule.split('||'):
							if self.check_rule(_rule, title, body, header):
								num += 1
								break
					else:
						if self.check_rule(rule, title, body, header):
							num += 1
				if num == len(key.split('&&')):
					return name

	def run(self):
		try:
			header, body, title = self.get_info()
			for _id in xrange(1, int(count())):
				try:
					if self.result == '':
						self.result = "["+self.handle(_id, header, body, title)+"]"
					else:
						self.result = self.result+"["+self.handle(_id, header, body, title)+"]"
				except Exception as e:
					pass
		except Exception as e:
			pass

def exploit(target, headers=None):
	if 'http://' in target or 'https://' in target:
		cms = CMSScanner(target)
		cms.run()
		return cms.result
	else:
		try:
			target = 'http://'+target
			cms = CMSScanner(target)
			cms.run()
			return cms.result
		except:
			target = 'https://'+target
			cms = CMSScanner(target)
			cms.run()
			return cms.result
