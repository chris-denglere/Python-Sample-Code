import pymysql
import sys
import appconfig
import datetime, decimal

class ErrorCode:
	SUCCESS = 0
	SESSION_TIMEOUT = 1
	GENERAL_ERROR = 2
	SQL_ERROR = 3

def fail(msg, error = ErrorCode.GENERAL_ERROR, data=None):
	return {"status" : False, "msg" : msg, "error_code" : error, "data" : data}

def success(data):
	return {"status" : True, "msg" : "OK", "error_code" : ErrorCode.SUCCESS, "data" : data}

def callDB(sql, params = None, dict=False, fetch=False):
	conn = None
	cur = None

	try:
		conn = pymysql.connect(*appconfig.db_params)
		conn.autocommit(True)
		if dict:
			cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
		else:
			cur = conn.cursor()

		if params:
			cur.execute(sql, params)
		else:
			cur.execute(sql)

		if fetch:
			data = cur.fetchall()
			for i in range(len(data)):
				for key in data[i]:
					if isinstance(data[i][key], datetime.datetime):
					 	data[i][key] = data[i][key].isoformat()
					elif isinstance(data[i][key], decimal.Decimal):
					 	data[i][key] = float(data[i][key])
			return data
		else:
			return cur
	except Exception, e:
		raise e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close();

def multiDB(sql):
	results = []
	for s in sql:
		results.append(callDB(s))
	return results

def selectDB(sql, params = None):
	result = callDB(sql, params=params, dict=True, fetch=True)
	if not result:
		result = []
	return success(result)