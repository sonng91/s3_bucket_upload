import info as inf
import pandas as pd
import psycopg2
import Staffing_s3_file as s3_file

# user and pw stored in a different file
user = inf.user
pw = inf.pw
path = r'//ant/dept/Redhawk/VendorManagement/Gateway Performance/Z WBR Correspondence/MOP-Staffing Air Vendor/CAMP MOP Staffing/'
savepath = r'//ant/dept/Redhawk/Performance/Tableau Source Files/Tableau Dashboards/Monday WBR reports/Final WBR Tableau Reports/MOP_Staffing_CAMP/'

conn = psycopg2.connect(
    host='amazonairbi.cbntrbaka6py.us-east-1.redshift.amazonaws.com',
    user=user,
    port=8192,
    password=pw,
    dbname='amazonairbi')


cur = conn.cursor()

filename = 'MOP_Staffing_Sheet.xlsx'

print("Converting file into csv file...")
# Opening MOP_Staffing_Sheet.xlsx then saving as csv in the save directory path
# the next few lines are turning the values into integers because pandas will cast them as floating numbers which will break the table
read_file = pd.read_excel(path + filename)
read_file = read_file.fillna(0)
read_file['Planned MOP'] =read_file['Planned MOP'].astype(int)
read_file['Headcount'] =read_file['Headcount'].astype(int)
read_file['Daily Planned Labor Hours'] =read_file['Daily Planned Labor Hours'].astype(int)
read_file['Labor Hours'] =read_file['Labor Hours'].astype(int)

read_file.to_csv (savepath + 'MOP_Staffing_Sheet_original.csv', index=None, header=True)
print("Saved into " + savepath + 'MOP_Staffing_Sheet_original.csv')


# NEED TO UPLOAD CSV FILE INTO S3 BUCKET HERE
print("Uploading csv file into gateway_ops s3 bucket...")
csv_file = pd.read_csv(savepath + 'MOP_Staffing_Sheet.csv')
csv_file = csv_file.fillna(0)
csv_file['Planned MOP'] =csv_file['Planned MOP'].astype(int)
csv_file['Headcount'] =csv_file['Headcount'].astype(int)
csv_file['Daily Planned Labor Hours'] =csv_file['Daily Planned Labor Hours'].astype(int)
csv_file['Labor Hours'] =csv_file['Labor Hours'].round(decimals=0).astype(int)
csv_file.to_csv (savepath + 'MOP_Staffing_Sheet.csv', index=None, header=True)
csv_file.to_csv (savepath + 'MOP_Staffing_Sheet_backup.csv', index=None, header=True)
s3_file.upload_to_aws(s3_file.file_name,s3_file.bucket_name, s3_file.s3_file_name)
print("Replaced old file with updated file")
# NEED TO UPLOAD CSV FILE INTO S3 BUCKET HERE

trunc_sql = """
TRUNCATE table air_gatewayops.mopstaffing_v2;
"""


# CURRENTLY NOT LOADING THE TABLE
loadingdata_sql = """
copy air_gatewayops.mopstaffing_v2 -- table to load into 
from 's3://air-gatewayops/mop_staffing/MOP_Staffing_Sheet.csv'  -- path of file to load
iam_role 'arn:aws:iam::841631579559:role/amazonairbi_readwrite_s3'
delimiter ',' -- usually ','
BLANKSASNULL -- this loads blank files as NULL values. if you don't have this, blank values will load as an empty string for VARCHAR/CHAR ('')
IGNOREHEADER 1 -- only include this if your csv/tsv has the column headers as the first line;
"""

result = """
Select count(1) from air_gatewayops.mopstaffing_v2
"""


def move_to_loading_new_data_into_table():
    ans = input("Please upload file into s3 bucket. Press Y when ready.")
    return ans

if __name__ == '__main__':
    print("Starting..")

    #if move_to_loading_new_data_into_table() == 'Y':
        # truncating table because when loading the updated s3 file,
        # it will append to the table not replace which will cause duplicates.
        # this will prevent duplicates

    print("TRUNCATING staffing table...")
    cur.execute(trunc_sql)

        # LOADS S3 FILE INTO THE MOP STAFFING TABLE
    print("loading s3 file into the MOP staffing table")
    #try:
        #engine.execute(loadingdata_sql)
    cur.execute(loadingdata_sql)
    #except:
    #    print('error when loading s3 data into table')

    # LOADING RESULT OF THE s3 FILE
    print("printing results...")
    cur.execute(result)

    records = cur.fetchall()

    for row in records:
        cnt_rows = row[0]
    print("Total number of rows is: ", cnt_rows)                                