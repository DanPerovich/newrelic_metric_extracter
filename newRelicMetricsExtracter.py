#!/usr/bin/env python

import requests, argparse, time, datetime

#Collection of AppID's and each's metrics to be pulled from the API
querySet = ['2191140,HttpDispatcher,requests_per_minute',
            '2191140,HttpDispatcher,average_response_time',
            '2191140,Errors/all,error_count',
            '2191140,Memory/Physical,used_mb_by_host',
            '2191140,Memory/Used,used_mb_by_host',
            '2191140,CPU/User Time,percent',
            '2176732,HttpDispatcher,requests_per_minute',
            '2176732,HttpDispatcher,average_response_time',
            '2176732,Errors/all,error_count',
            '2176732,Memory/Physical,used_mb_by_host',
            '2176732,Memory/Used,used_mb_by_host']

log_info = ''
log_debug = ''

localtime = datetime.datetime.utcnow()
splitDateTime = str(localtime).split(' ')
splitTime = splitDateTime[1].split(':')
dfltFromTime = splitDateTime[0] + 'T' + str(int(splitTime[0])-1) + ':00:00+00:00'
dfltToTime = splitDateTime[0] + 'T' + splitTime[0] + ':00:00+00:00'

parser = argparse.ArgumentParser(description='Extract metric data from New Relic')
parser.add_argument('apikey', help='New Relic RPM Admin API Key')
parser.add_argument('--fromTime', help='Time to start data extract from in UTC with offset (ex. 2018-06-11T11:00:00+00:00) (default=current hour-1)', default=dfltFromTime)
parser.add_argument('--toTime', help='Time to end data extract at in UTC with offset (ex. 2018-06-11T12:00:00+00:00) (default=current hour)', default=dfltToTime)
parser.add_argument('-p', '--period', help='Number of seconds per datapoint. See https://docs.newrelic.com/docs/apis/rest-api-v2/requirements/extract-metric-timeslice-data#period (default=60)', default=60)
parser.add_argument('--printoutput', help='Print output file to screen in addition to file', action='store_true')
parser.add_argument('-d', '--debuglevel', help='Set the stdout debug level', choices=['info','debug'])
args = parser.parse_args()

api_key = args.apikey
fromTime = args.fromTime
toTime = args.toTime
period = args.period
print_output = args.printoutput

if args.debuglevel == 'info':
	log_info = True
	log_debug = False
elif args.debuglevel == 'debug':
	log_info = True
	log_debug = True
else:
	log_info = False
	log_debug = False

if log_info: print('api_key: ' + api_key)
if log_info: print('fromTimeTime: ' + dfltFromTime)
if log_info: print('toTime: ' + toTime)
if log_info: print('period: ' + str(period))
if log_info: print('print_output: ' + str(print_output))
if log_info: print('debuglevel: ' + args.debuglevel)

api_headers = {'X-Api-Key': api_key}

def runQuery( appId, metricName, value, fromT, toT, period ):
  # Get the application Name associated with the appId
  response = requests.get('https://api.newrelic.com/v2/applications/' + str(appId) + '.json', headers=api_headers)
  if response.status_code == requests.codes.ok:
    if log_info: print ('Success: api call for ' + str(appId))
    if log_debug: print ('API result is: ' + response.text)
    rsp_json = response.json()
    appName = rsp_json['application']['name']
  else:
    print('FAILED: api call for appName for ' + str(apdId))
    print(response.status_code)
    appName = '<api error>'

  # Execute the query for the defined application, metric, timeframe, and granularity
  parameters = {'names[]': metricName, 'values[]': value, 'from': fromT, 'to': toT, 'period': period}
  response = requests.get('https://api.newrelic.com/v2/applications/' + str(appId) + '/metrics/data.json', headers=api_headers, params=parameters)
  if response.status_code == requests.codes.ok:
    if log_info: print ('Success: api call for ' + str(appId) + ':' + metricName + ':' + value)
    if log_debug: print ('API result is: ' + response.text)
    rsp_json = response.json()
    data = rsp_json['metric_data']
    result = 'appId,appName,metricName,value,from,to,datapoint'
    for metric in data['metrics']:
    	for timeslice in metric['timeslices']:
      		result += '\n' + str(appId) + ',' + appName + ',' + metricName + ',' + str(value) + ',' + timeslice['from'] + ',' + timeslice['to'] + ',' + str(timeslice['values'][value])
    if log_debug: print('Result='+result)
    if print_output: print('Output of api call for ' + str(appId) + ':' + metricName + ':' + value + '\n' + result)
    file = open(cleanFilename(str(appId) + '-' + appName + '-' + metricName + '-' + value + '-' + fromT) + '.csv','w')
    file.write(result)
    file.close()

  else:
  	print('FAILED: api call for ' + str(apdId) + ':' + metricName + ':' + value)
  	print(response.status_code)
  return

def cleanFilename( oldFilename ):
  newFilename = oldFilename.replace(':','_')
  newFilename = newFilename.replace('/','_')
  newFilename = newFilename.replace('\\','_')
  return newFilename


print('Script start')

##Run Queries
for i in querySet:
  record = i.split(',')
  app=record[0]
  metric=record[1]
  value=record[2]
  runQuery(app,metric,value,fromTime,toTime,period)
  if log_debug: print('Sleeping for 1 second')
  time.sleep(1)
print('Script end')
