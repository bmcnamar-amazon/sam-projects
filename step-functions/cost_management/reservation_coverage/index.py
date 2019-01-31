import datetime
from dateutil.relativedelta import relativedelta
import sys

import boto3

client = boto3.client('ce')

end = datetime.date.today().replace(day=1)
start = (datetime.date.today() - relativedelta(months=+1)).replace(day=1) #1st day of month 1 months ago

services = [
                'Amazon Elastic Compute Cloud - Compute', 'Amazon Relational Database Service', 'Amazon Redshift',
                'Amazon ElastiCache', 'Amazon Elasticsearch Service'
    ]

def handler(event=None, context=None):
    coverage = {}

    for service in services:
        print 'Working on {}...'.format(service)
        try:
            response = client.get_reservation_coverage(
                TimePeriod={
                    'Start': start.isoformat(),
                    'End': end.isoformat()
                },
                Metrics=[
                    'Hour', # Hour, Unit, Cost
                ],
                Filter={
                    'Dimensions': {
                        'Key': 'SERVICE',
                        'Values': [ 
                            service 
                        ]
                    }
                },
                GroupBy=[{"Type": "DIMENSION","Key": "REGION"}] # AZ, INSTANCE_TYPE, LINKED_ACCOUNT, PLATFORM, REGION, TENANCY
            )
        except Exception as e:
            print 'Error gathering reservation coverage: {}'.format(str(e))
            sys.exit(1)
    
        coverage[service] = response['CoveragesByTime']

    print coverage
    return coverage
    

if __name__ == '__main__':
    handler()

