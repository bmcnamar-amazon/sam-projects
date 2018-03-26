import boto3
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys

s3 = boto3.resource('s3')

output_bucket = os.environ['OUTPUT_BUCKET']
bucket_keyspace = 'report'

def handler(event, context):
    report_date = event['date']

    print 'Report date: {}'.format(report_date)
    for customer in event['customers']:
            name = customer['name']
            ticker = customer['ticker']
            link = customer['url']
            print 'Working on {}...'.format(customer['name'])

            try:
                report_directory = '/tmp'
                report_name = '{}.pdf'.format(customer['name'].replace(' ','_'))
                full_report = report_directory + '/' + report_name
                print 'Creating report {}'.format(report_name)
                c = canvas.Canvas(full_report, pagesize=letter)
                c.drawString(100,750,"FINANCIAL REPORT")
                c.drawString(100,735,"Prepared by: Research Function ({})".format(report_date))
                c.drawString(100,700,"Customer: {}".format(name))
                c.drawString(100,685,"Ticker: {}".format(ticker))
                c.drawString(100,670,"Information URL: {}".format(link))
                c.save()
                print 'Saving report {} to s3://{}/{}/{}'.format(report_name, output_bucket, bucket_keyspace, report_name)
                s3.meta.client.upload_file(full_report, output_bucket, '{}/{}'.format(bucket_keyspace, report_name))
            except Exception as e:
                print 'FAILURE creating and saving report for {}: {}'.format(customer['name'], str(e))
                sys.exit(1)
    print 'Report generation complete'
    return 'Report generation complete'
