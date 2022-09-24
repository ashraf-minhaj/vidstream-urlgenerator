""" Get new s3 objects and create cloudfront url and store in db.

 author: Ashraf Minhaj
 mail  : ashraf_minhaj@yahoo.com

(c) Ashraf Minhaj
"""

import json
import logging
import boto3
import configparser


# initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    
    logger.info(f"request got {event}")
    logger.info("Event type:")
    logger.info(type(event))

    # get file/object name
    media_object = event['Records'][0]['s3']['object']['key']
    logger.info('file object:')
    logger.info(media_object)

    # every milisecond costs, so we check the file type at first
    # to decide it's worth proceeeding or not.
    # check file type and continue operation
    if media_object.split('.')[-1] != 'mp4':
        logger.info("It's not a mp4 file bro. we should quit.")
        return {
        'statusCode': 415,
        'body': json.dumps("Unsupported Media: can not convert, file is not in mp4 format.")
        }

    
    # variables
    response_status = 500
    response_text = "Server side error, check logs."

    # get input bucket
    input_bucket_name = event['Records'][0]['s3']['bucket']['name']
    logger.info("Input bucket:")
    logger.info(input_bucket_name)

    # read config.ini files for critical/confidential data
    logger.info('File is mp4, cont... Reading Config Variables')
    config = configparser.ConfigParser()
    config.read('config.ini')

    logger.info("Getting necessary data from config file")
    config_data        = config['default']
    cloudfront_url     = config_data['cloudfront_url']
    # destination_bucket = config_data['destination_bucket']

    logger.info(f"Main cloudfront url from config: {cloudfront_url}")

    # prepare url
    logger.info("Preparing url for db")
    # template: 's3://vidstream-processed-videos/fileName.ext'
    object_url = f'{cloudfront_url}/{media_object}'

    logger.info("final object url with cloudfront: ")
    logger.info(object_url)

    # connect to dynamo db
    # object_name: category_fileName_resolution.mp4
    # exmp:  python.string.360p.mp4
    resolution = media_object.split('.')[-2]
    logger.info("Getting media resolution")
    logger.info(resolution)

    # open json mediaconvert job template
    logger.info("Reading collection json file")
    with open("collection.json", "r") as jsonfile:
        collection_object = json.load(jsonfile)
        logger.info(collection_object)

    # edit the collection object
    logger.info("Editing collection obj")
    collection_object['category'] = media_object.split('.')[0]
    collection_object[resolution] = object_url

    logger.info("Updated collection to be pu")
    logger.info(collection_object)

    # read collections and store in db
    logger.info("Init boto client and connecting with table")
    db_table = boto3.resource('dynamodb').Table("vidstream-urldb")  # connecting with table
    logger.info("Connection with table: Success")
    logger.info(f"Table status {db_table.table_status}")

    # basic put item
    try:
        res = db_table.put_item(Item=collection_object)
        response_status = res["ResponseMetadata"]["HTTPStatusCode"]
        if  response_status == 200:
            response_status = 200
            response_text = "Everything went well"
        else:
            response_text = "Put item failed"
    except Exception as e:
        logger.exception(e)
   
    return {
        'statusCode': response_status,
        'body': json.dumps(response_text)
    }

