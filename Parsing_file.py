import info as inf
import pandas as pd
import sqlalchemy as alc

user = inf.user
pw = inf.pw
path = r'//ant/dept/Redhawk/VendorManagement/Gateway Performance/Z WBR Correspondence/MOP-Staffing Air Vendor/CAMP MOP Staffing/'
savepath = r'//ant/dept/Redhawk/Performance/Tableau Source Files/Tableau Dashboards/Monday WBR reports/Final WBR Tableau Reports/MOP_Staffing_CAMP/'

filename = 'MOP_Staffing_Sheet.xlsx'

# Opening MOP_Staffing_Sheet.xlsx then saving as csv in the save directory path
read_file = pd.read_excel (path + filename)

read_file = read_file.dropna()
read_file['Planned MOP'] =read_file['Planned MOP'].astype(int)
read_file['Headcount'] =read_file['Headcount'].astype(int)
read_file['Daily Planned Labor Hours'] =read_file['Daily Planned Labor Hours'].astype(int)
read_file['Labor Hours'] =read_file['Labor Hours'].astype(int)


#{'planned_headcount': int, 'headcount': int, 'daily_plan' : int, 'labor_hours' : int}

read_file.to_csv(savepath + 'MOP_Staffing_Sheet.csv', index = None, header=True)