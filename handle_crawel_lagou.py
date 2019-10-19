import requests
import re
import time
import json
import multiprocessing
from handle_insert_data import lagou_mysql


class HandleLaGou(object):
	def __init__(self):
		# 使用session保存cookie信息
		self.lagou_session = requests.session()
		self.header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}
		self.city_list = ""
	
	# 获取城市列表
	def handle_city(self):
		city_search = re.compile(r'zhaopin/">(.*?)</a>')
		city_url = "https://www.lagou.com/jobs/allCity.html"
		city_result = self.handle_request(method="GET", url=city_url)
		self.city_list = city_search.findall(city_result)
		self.lagou_session.cookies.clear()
	
	def handle_city_job(self, city):
		first_request_url = "https://www.lagou.com/jobs/list_web?city=%s&cl=false&fromSearch=true&labelWords=sug&suginput=web" % city
		first_response = self.handle_request(method="GET", url=first_request_url)
		total_page_search = re.compile(r'span\stotalNum">(\d+)</span>')
		try:
			total_page = total_page_search.search(first_response).group(1)
		except:
			return
		else:
			for i in range(1, int(total_page) + 1):
				data = {
					"pn": i,
					"kd": "web"
				}
				page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
				referer_url = "https://www.lagou.com/jobs/list_web?city=%s&cl=false&fromSearch=true&labelWords=sug&suginput=web" % city
				# referer的url需要进行encode
				self.header['Referer'] = referer_url.encode()
				response = self.handle_request(method="POST", url=page_url, data=data, info=city)
				lagou_data = json.loads(response)
				job_list = lagou_data['content']['positionResult']['result']
				for job in job_list:
					lagou_mysql.insert_item(job)
	
	# 请求方法
	def handle_request(self, method, url, data=None, info=None):
		while True:
			# 加入代理
			proxyinfo = "http://%s:%s@%s:%s" % ('', '', '116.208.53.131', '9999')
			proxy = {
				"http": proxyinfo,
				"https": proxyinfo
			}
			try:
				if method == "GET":
					response = self.lagou_session.get(url=url, headers=self.header)
				elif method == "POST":
					response = self.lagou_session.post(url=url, headers=self.header, data=data)
			except:
				# 需要先清除cookies信息
				self.lagou_session.cookies.clear()
				# 重新获取cookies信息
				first_request_url = "https://www.lagou.com/jobs/list_web?city=%s&cl=false&fromSearch=true&labelWords=sug&suginput=web" % info
				self.handle_request(method="GET", url=first_request_url)
				time.sleep(10)
				continue
			response.encoding = "utf-8"
			if '频繁' in response.text:
				print(response.text)
				# 需要先清除cookies信息
				self.lagou_session.cookies.clear()
				# 重新获取cookies信息
				first_request_url = "https://www.lagou.com/jobs/list_web?city=%s&cl=false&fromSearch=true&labelWords=sug&suginput=web" % info
				self.handle_request(method="GET", url=first_request_url)
				time.sleep(10)
				continue
			return response.text


if __name__ == "__main__":
	lagou = HandleLaGou()
	lagou.handle_city()
	# 引入多进程
	pool = multiprocessing.Pool(2)
	for city in lagou.city_list:
		pool.apply_async(lagou.handle_city_job, args=(city,))
	pool.close()
	pool.join()
