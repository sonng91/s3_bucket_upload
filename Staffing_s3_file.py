import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'ACCESSKEY'
SECRET_KEY = 'SECRETKEY'

file_name = r'//ant/dept/Redhawk/Performance/Tableau Source Files/Tableau Dashboards/Monday WBR reports/Final WBR Tableau Reports/MOP_Staffing_CAMP/MOP_Staffing_Sheet.csv'
bucket_name = 'air-gatewayops'
s3_file_name = 'mop_staffing/MOP_Staffing_Sheet.csv'
#s3://air-gatewayops/mop_staffing/MOP_Staffing_Sheet.csv


def upload_to_aws(file_name, bucket, s3_file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_file_name: S3 object name. 
    :return: True if file was uploaded, else False
    """

    try:
        s3.upload_file(file_name, bucket, s3_file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

#uploaded = upload_to_aws(file_name, bucket_name, s3_file_name)