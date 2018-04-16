import os

def handler(event, context):
    print "URL: {}".format(os.getenv('URL'))
    return "URL: {}".format(os.getenv('URL'))
