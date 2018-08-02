import boto3
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import sys

s3 = boto3.resource('s3')

output_bucket = os.environ['OUTPUT_BUCKET']
bucket_keyspace = 'report'
url = 'http://asap-image-tank.s3-website-us-east-1.amazonaws.com'

def handler(event, context):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_file = event['Records'][0]['s3']['object']['key']

    try:
        s3.Bucket(input_bucket).download_file(input_file, '/tmp/{}'.format(input_file))
    except Exception as e:
        print 'Error: {}'.format(str(e))
        sys.exit(1)

    data = json.load(open('/tmp/{}'.format(input_file)))

    report_date = data['date']

    print 'Report date: {}'.format(report_date)
    for customer in data['customers']:
            name = customer['name']
            ticker = customer['ticker']
            link = customer['url']
            if customer['logo']:
                image_url = '{}/{}'.format(url, customer['logo'])
            else:
                image_url = '{}/{}'.format(url, 'AMZN.jpg')
            print 'Working on {}...'.format(customer['name'])

            try:
                report_directory = '/tmp'
                report_name = '{}.pdf'.format(customer['name'].replace(' ','_'))
                full_report = report_directory + '/' + report_name
                print 'Creating report {}'.format(report_name)

                logo = ImageReader(image_url)

                c = canvas.Canvas(full_report, pagesize=letter)
                c.drawString(100,750,"FINANCIAL REPORT")
                c.drawString(100,735,"Prepared by: Research Function ({})".format(report_date))
                c.drawString(100,700,"Customer: {}".format(name))
                c.drawString(100,685,"Ticker: {}".format(ticker))
                c.drawString(100,670,"Information URL: {}".format(link))
                c.drawImage(logo, 500, 670, width=100, height=100, mask='auto')
                c.save()
                print 'Saving report {} to s3://{}/{}/{}'.format(report_name, output_bucket, bucket_keyspace, report_name)
                s3.meta.client.upload_file(full_report, output_bucket, '{}/{}'.format(bucket_keyspace, report_name))
            except Exception as e:
                print 'FAILURE creating and saving report for {}: {}'.format(customer['name'], str(e))
                continue
    
    print 'Report generation complete'
    return 'Report generation complete'
