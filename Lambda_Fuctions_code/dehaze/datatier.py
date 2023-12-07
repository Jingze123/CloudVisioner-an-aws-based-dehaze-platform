import boto3
import cv2
import numpy as np
import os
import urllib.parse
import pathlib
from configparser import ConfigParser
import datatier
import uuid

# initialize
s3 = boto3.resource('s3')

config_file = 'config.ini'
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
configur = ConfigParser()
configur.read(config_file)


def dark_channel(im, sz):
    """Calculate the dark channel of the image"""
    b, g, r = cv2.split(im)
    dc = cv2.min(cv2.min(r, g), b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
    dark = cv2.erode(dc, kernel)
    return dark


def atm_light(im, dark):
    """Estimating global atmospheric light intensity"""
    [h, w] = im.shape[:2]
    top_pixels = int(max(h * w * 0.001, 1))
    darkvec = dark.reshape(h * w)
    imvec = im.reshape(h * w, 3)

    indices = darkvec.argsort()[::-1][:top_pixels]
    atmsum = np.mean(imvec[indices], axis=0)
    return atmsum


def transmission_estimate(im, A, sz):
    """Estimated transmission diagram"""
    omega = 0.95
    im3 = np.empty(im.shape, im.dtype)
    for i in range(3):
        im3[:, :, i] = im[:, :, i] / A[i]
    transmission = 1 - omega * dark_channel(im3, sz)
    return transmission


def guided_filter(I, p, r, eps):
    """Guided filtering for optimizing transmission graphs"""
    return cv2.bilateralFilter(p, d=r, sigmaColor=eps, sigmaSpace=eps)


def recover(im, t, A, tx=0.1):
    """Restore image from estimated atmospheric light and transmission map"""
    res = np.empty(im.shape, im.dtype)
    t = np.maximum(t, tx)
    for i in range(3):
        res[:, :, i] = (im[:, :, i] - A[i]) / t + A[i]
    return res


def lambda_handler(event, context):
    try:
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')

        print("**STARTING**")
        print("**lambda: image_dehaze**")

        # get s3_bucket_name and file_name
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        bucketkey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # check extension
        extension = pathlib.Path(bucketkey).suffix
        if extension.lower() != ".jpg" and extension.lower() != ".jpeg":
            raise Exception("Expecting S3 document to be a JPEG image")

        print(f"Processing image: {bucketkey}")
        print(f"os.path.basename(bucketkey)", {os.path.basename(bucketkey)})

        # download to /tmp/
        local_filename = "/tmp/" + os.path.basename(bucketkey)
        print(f"localname", {local_filename})
        print(f"bucketname", {bucket_name})
        s3.Bucket(bucket_name).download_file(bucketkey, local_filename)

        # read image
        image_np = cv2.imread(local_filename)
        print("***Dehazing***")

        # dehaze
        # tranform to float32
        I = image_np.astype('float32') / 255

        # Calculate the dark channel of the image
        dark = dark_channel(I, 15)

        # Estimating global atmospheric light intensity
        A = atm_light(I, dark)

        # Estimated transmission diagram
        te = transmission_estimate(I, A, 15)

        # Guided filtering for optimizing transmission graphs
        t = guided_filter(I, te, 60, 0.0001)

        # Recover images
        J = recover(I, t, A, 0.1)
        print("***Processing Successed***")

        output_key = output_key = "/".join(bucketkey.split('/')[:-2]) + '/result/' + str(uuid.uuid4()) + '.jpg'

        # Convert the processed image back to a byte stream and save it
        result_filename = "/tmp/result.jpeg"
        cv2.imwrite(result_filename, np.uint8(J * 255))

        print("***uploading***")
        s3.Bucket(bucket_name).upload_file(result_filename, output_key, ExtraArgs={'ContentType': 'image/jpeg'})
        # update db
        def update_database_on_success(endpoint, portnum, username, pwd, dbname, datafilekey, resultsfilekey):
            dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)
            try:
                sql = "UPDATE jobs SET status = %s, resultsfilekey = %s WHERE datafilekey = %s"
                datatier.perform_action(dbConn, sql, ['completed', resultsfilekey, datafilekey])
            finally:
                dbConn.close()

        update_database_on_success(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname, bucketkey,
                               output_key)



        return {
            'statusCode': 200,
            'body': f'Image processed and saved as {output_key}'
        }

    except Exception as e:
        output_key = "/".join(bucketkey.split('/')[:-2]) + '/result/' + str(uuid.uuid4()) + '.jpg'
        print(f"Error processing image: {str(e)}")
        def update_database_on_error(endpoint, portnum, username, pwd, dbname, datafilekey, resultsfilekey):
            dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)
            try:
                sql = "UPDATE jobs SET status = %s, resultsfilekey = %s WHERE datafilekey = %s"
                datatier.perform_action(dbConn, sql, ['error', resultsfilekey, datafilekey])
            finally:
                dbConn.close()
        update_database_on_error(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname, bucketkey,
                            output_key)

        return {
            'statusCode': 500,
            'body': str(e)
        }
