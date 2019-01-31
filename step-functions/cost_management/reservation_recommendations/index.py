import datetime
import os
import sys

import boto3

client = boto3.client('ce')

# 

def handler(event=None, context=None):
    recommendations = {}
    recommendations['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    recommendations['reservation_recommendations'] = []

    services = [
                'Amazon Elastic Compute Cloud - Compute', 'Amazon Relational Database Service', 'Amazon Redshift',
                'Amazon ElastiCache', 'Amazon Elasticsearch Service'
    ]

    for service in services:
        print 'Working on {}...'.format(service)
        try:
            response = client.get_reservation_purchase_recommendation(
                    LookbackPeriodInDays='SIXTY_DAYS',
                    TermInYears='ONE_YEAR',
                    PaymentOption='ALL_UPFRONT',
                    Service=service
                )
        except Exception as e:
            print 'Error gathering recommendations for {}: {}'.format(service, str(e))
            sys.exit(1)

        if len(response['Recommendations']) == 0:
            statement = {service: 'None'}
        else:
            statement = {service: response['Recommendations']}
        recommendations['reservation_recommendations'].append(statement)
    
    print recommendations
    return recommendations

if __name__ == '__main__':
    handler()
