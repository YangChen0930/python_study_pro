from collections import Counter

from sqlalchemy import func

from create_lagou_tables import Lagoutables
from create_lagou_tables import Session
import time


class HandleLagouData(object):
	def __init__(self):
		self.mysql_session = Session()
		# self.date = '2019-06-24'
	
		self.date = time.strftime("%Y-%m-%d", time.localtime())
	
	# 数据存储
	def insert_item(self, item):
		date = time.strftime("%Y-%m-%d", time.localtime())
		data = Lagoutables(
			# 岗位id
			positionID=item['positionId'],
			# 经度
			longitude=item['longitude'],
			# 纬度
			latitude=item['latitude'],
			# 岗位名称
			positionName=item['positionName'],
			# 工作年限
			workYear=item['workYear'],
			# 学历
			education=item['education'],
			# 岗位性质
			jobNature=item['jobNature'],
			# 公司类型
			financeStage=item['financeStage'],
			# 公司规模
			companySize=item['companySize'],
			# 业务方向
			industryField=item['industryField'],
			# 所在城市
			city=item['city'],
			# 岗位标签
			positionAdvantage=item['positionAdvantage'],
			# 公司简称
			companyShortName=item['companyShortName'],
			# 公司全称
			companyFullName=item['companyFullName'],
			# 公司所在区
			district=item['district'],
			# 公司福利标签
			companyLabelList=','.join(item['companyLabelList']),
			salary=item['salary'],
			# 抓取日期
			crawl_date=date
		)
		
		# 存储数据之前，先查询表里是否有这条岗位信息
		query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date == date,
																	Lagoutables.positionID == item[
																		'positionId']).first()
		
		if query_result:
			print('该岗位信息已存在%s:%s:%s' % (item['positionId'], item['city'], item['positionName']))
		else:
			# 插入数据
			self.mysql_session.add(data)
			# 提交到数据库
			self.mysql_session.commit()
			print('新增岗位信息%s' % item['positionId'])
	
	# 行业信息
	def query_industryfield_result(self):
		info = {}
		# 查询今日抓取到的行业信息数据
		result = self.mysql_session.query(Lagoutables.industryField).filter(
			Lagoutables.crawl_date == self.date
		).all()
		result_list1 = [x[0].split(',')[0] for x in result]
		result_list2 = [x for x in Counter(result_list1).items() if x[1] > 10]
		# 填充的是series里面的data
		data = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in data]
		info['x_name'] = name_list
		info['data'] = data
		return info
	
	# 薪资情况
	def query_salary_result(self):
		info = {}
		# 查询今日抓取到的薪资数据
		result = self.mysql_session.query(Lagoutables.salary).filter(
			Lagoutables.crawl_date == self.date
		).all()
		result_list1 = [x[0].split('-')[0] for x in result]
		result_list2 = [x for x in Counter(result_list1).items() if x[1] > 10]
		# 填充的是series里面的data
		data = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in data]
		info['x_name'] = name_list
		info['data'] = data
		return info
	
	# 融资情况
	def query_financeStage_result(self):
		info = {}
		# 查询今日抓取到的融资数据
		result = self.mysql_session.query(Lagoutables.financeStage).filter(
			Lagoutables.crawl_date == self.date
		).all()
		result_list1 = [x[0] for x in result]
		result_list2 = [x for x in Counter(result_list1).items()]
		# 填充的是series里面的data
		data = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in data]
		info['x_name'] = name_list
		info['data'] = data
		return info
	
	# 公司规模
	def query_companySize_result(self):
		info = {}
		# 查询今日抓取到的融资数据
		result = self.mysql_session.query(Lagoutables.companySize).filter(
			Lagoutables.crawl_date == self.date
		).all()
		result_list1 = [x[0] for x in result]
		result_list2 = [x for x in Counter(result_list1).items()]
		# 填充的是series里面的data
		data = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in data]
		info['x_name'] = name_list
		info['data'] = data
		return info
	
	# 岗位要求
	def query_jobNature_result(self):
		info = {}
		# 查询今日抓取到的融资数据
		result = self.mysql_session.query(Lagoutables.jobNature).filter(
			Lagoutables.crawl_date == self.date
		).all()
		result_list1 = [x[0] for x in result]
		result_list2 = [x for x in Counter(result_list1).items()]
		# 填充的是series里面的data
		data = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in data]
		info['x_name'] = name_list
		info['data'] = data
		return info
	
	# 岗位发布数
	def query_job_result(self):
		info = {}
		result = self.mysql_session.query(Lagoutables.crawl_date, func.count('*').label('c')).group_by(
			Lagoutables.crawl_date).all()
		result1 = [{"name": x[0], "value": x[1]} for x in result]
		name_list = [name['name'] for name in result1]
		info['x_name'] = name_list
		info['data'] = result1
		return info
	
	# 工作经验
	def query_workYear_result(self):
		info = {}
		# 查询今日抓取到的工作年限数据
		result = self.mysql_session.query(Lagoutables.workYear).filter(Lagoutables.crawl_date == self.date).all()
		# 处理原始数据
		result_list1 = [x[0] for x in result]
		# 计数,并返回
		result_list2 = [x for x in Counter(result_list1).items()]
		result = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in result]
		info['x_name'] = name_list
		info['data'] = result
		return info
	
	def query_education_result(self):
		info = {}
		# 查询今日抓取到的学历数据
		result = self.mysql_session.query(Lagoutables.education).filter(Lagoutables.crawl_date == self.date).all()
		# 处理原始数据
		result_list1 = [x[0] for x in result]
		# 计数,并返回
		result_list2 = [x for x in Counter(result_list1).items()]
		result = [{"name": x[0], "value": x[1]} for x in result_list2]
		name_list = [name['name'] for name in result]
		info['x_name'] = name_list
		info['data'] = result
		return info
	
	def query_city_result(self):
		info = {}
		# 查询今日抓取到的数据
		result = self.mysql_session.query(Lagoutables.city, func.count('*').label('c')).filter(
			Lagoutables.crawl_date == self.date).group_by(Lagoutables.city).all()
		result1 = [{"name": x[0], "value": x[1]} for x in result]
		name_list = [name['name'] for name in result1]
		info['x_name'] = name_list
		info['data'] = result1
		return info
	
	# 抓去数量
	def count_result(self):
		info = {}
		info['all_count'] = self.mysql_session.query(Lagoutables).count()
		info['today_count'] = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date == self.date).count()
		return info


lagou_mysql = HandleLagouData()
