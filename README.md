# newrelic_metric_extracter
Python script used to extract APM metrics into csv files

required packages: requests

```
usage: newRelicMetricsExtracter.py [-h] [--fromTime FROMTIME]
                                   [--toTime TOTIME] [-p PERIOD]
                                   [--printoutput] [-d {info,debug}]
                                   apikey

Extract metric data from New Relic

positional arguments:
  apikey                New Relic RPM Admin API Key

optional arguments:
  -h, --help            show this help message and exit
  --fromTime FROMTIME   Time to start data extract from in UTC with offset
                        (ex. 2018-06-11T11:00:00+00:00) (default=current
                        hour-1)
  --toTime TOTIME       Time to end data extract at in UTC with offset (ex.
                        2018-06-11T12:00:00+00:00) (default=current hour)
  -p PERIOD, --period PERIOD
                        Number of seconds per datapoint. See
                        https://docs.newrelic.com/docs/apis/rest-
                        api-v2/requirements/extract-metric-timeslice-
                        data#period (default=60)
  --printoutput         Print output file to screen in addition to file
  -d {info,debug}, --debuglevel {info,debug}
                        Set the stdout debug level
```
