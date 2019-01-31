import datetime
from dateutil.relativedelta import relativedelta
import sys

import boto3

client = boto3.client('ce')

end = datetime.date.today().replace(day=1)
start = (datetime.date.today() - relativedelta(months=+12)).replace(day=1) #1st day of month 12 months ago


def handler(event=None, context=None):
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start.isoformat(),
                'End': end.isoformat()
            },
            Granularity='MONTHLY',
            Metrics=[
                'UnblendedCost',
            ],
            GroupBy=[{"Type": "DIMENSION","Key": "SERVICE"}]
        )
    except Exception as e:
        print 'Error gathering recommendations for {}: {}'.format(service, str(e))
        sys.exit(1)
    
    print response['ResultsByTime']
    return response['ResultsByTime']

if __name__ == '__main__':
    handler()
