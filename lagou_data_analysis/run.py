from flask import Flask, render_template, jsonify
from handle_insert_data import lagou_mysql

# flask实例化
app = Flask(__name__)


@app.route("/")
def index():
	return "helllo world"


@app.route("/get_echart_data")
def get_echart_data():
	info = {}
	info['echart_1'] = lagou_mysql.query_industryfield_result()
	info['echart_2'] = lagou_mysql.query_salary_result()
	info['echart_31'] = lagou_mysql.query_financeStage_result()
	info['echart_32'] = lagou_mysql.query_companySize_result()
	info['echart_33'] = lagou_mysql.query_jobNature_result()
	info['echart_4'] = lagou_mysql.query_job_result()
	info['echart_5'] = lagou_mysql.query_workYear_result()
	info['echart_6'] = lagou_mysql.query_education_result()
	info['map'] = lagou_mysql.query_city_result()
	return jsonify(info)


@app.route("/lagou/", methods=['GET', 'POST'])
def lagou():
	result = lagou_mysql.count_result()
	return render_template('index.html', result=result)


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=8080)
