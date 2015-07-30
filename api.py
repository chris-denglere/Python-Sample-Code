import sys, os

# gets the directory name where the current file (api.wsgi) lives
pwd = os.path.dirname(__file__)
# change directory to pwd
os.chdir(pwd)
# append the pwd to sys.path
sys.path.append(pwd)

import db
from db import fail, success, ErrorCode
import appconfig
import types
import datetime
import decimal
import uuid
import bottle
from bottle import route, get, post, request, response, run
import traceback

# enable cross origin resource sharing (cors)
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
 
        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)
    return _enable_cors

# query
def getTotalUInUse(req):
	query = ""
	return db.selectDB(query)

# query
def getTotalTilesInUse(req):
	query = ""
	return db.selectDB(query)

#query
def getPercentTilesInUse(req):
	query = ""
	return db.selectDB(query)

# query
def getCurrentAvailableSpace(req):
	query = ""
	return db.selectDB(query)

# query
def getTilesAvailableforConsumptionbyMonth(req):
	query = ""
	return db.selectDB(query)

# query
def getPercentTilesAvailableforConsumption(req):
	query = ""
	return db.selectDB(query)

# query
def getPercentTilesInUse(req):
	query = "
	return db.selectDB(query)

# query
def getThirdTableDataPoints(req):
	query = 
	return db.selectDB(query)

actions = {
	'getTotalUInUse' : [getTotalUInUse],
	'getTotalTilesInUse' : [getTotalTilesInUse],
	'getPercentTilesInUse' : [getPercentTilesInUse],
	'getCurrentAvailableSpace' : [getCurrentAvailableSpace],
	'getTilesAvailableforConsumptionbyMonth' : [getTilesAvailableforConsumptionbyMonth],
	'getPercentTilesAvailableforConsumption' : [getPercentTilesAvailableforConsumption],
	'getPercentTilesInUse' : [getPercentTilesInUse],
	'getThirdTableDataPoints' : [getThirdTableDataPoints]
	}

@route('/')
def welcome():
	return "Welcome to the Data Warehouse API. Please use POST JSON API calls only."

# these decorators are needed to enable cors
@route('/', method=['OPTIONS', 'POST'])
@enable_cors
def api():
	try:
		req = request.json
		response.content_type = 'application/json'
		if 'action' in req:
			if req['action'] in actions:
				action = actions[req['action']]
				return action[0](req)
			else:
				return fail("Invalid action.")
		else:
			return fail("Invalid request data.")
	except:
		print traceback.format_exc()
		return fail('Failure in the api', data = traceback.format_exc())

application = bottle.default_app()

# this is for running the local WSGI web server for testing purposes
# run(host='localhost', port=8080, debug=True)
