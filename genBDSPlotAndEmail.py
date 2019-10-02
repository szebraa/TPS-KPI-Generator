#kick off cron at 10:31am everyday to process both fdsa and bdsa TPS KPI Default values: start time = 2:00PM (EST) , end time = 6:30PM (EST), date = yesterday , email = SDMsquad@bell.ca, sample int = 5s
#!/usr/bin/python
#!/bin/chmod

import sys, os, datetime
import pandas as pd

def giveDate(subtractBy,spec1,spec2,spec3,aString):
    date = datetime.datetime.now()- datetime.timedelta(days=subtractBy)
    return (date.strftime("%"+spec1) + aString + date.strftime("%"+spec2) + aString + date.strftime("%"+spec3))

#gets updates processed stats for BDSA
def getFileStats(dir,filename,date,start_time,end_time,sample_int,dict,date_index,tps_index,statsType):
    Query_stats = "Queries Processed"
    Updates_stats = "Updates Processed"
    if os.path.exists(dir + filename):
        fp = open(dir + filename)
        for k, line in enumerate(fp):
            if k > 11 and k<43212:
                tmp_arr = line.split(" ")
                tmp_arr = list(filter(None,tmp_arr))
                if tmp_arr[0] == date and tmp_arr[1] >= start_time and tmp_arr[1] <= end_time and int(tmp_arr[1].split(":")[2]) % sample_int == 0:
                    tmp = tmp_arr[1] + "(" + tmp_arr[0] + ")"
                    dict[date_index].append(tmp)
                    if statsType == Updates_stats:
                        tmp = tmp_arr[3]
                    if statsType == Query_stats:
                        tmp = tmp_arr[5]
                    dict[tps_index].append(tmp)
                else:
                    if tmp_arr[0] == date and tmp_arr[1] > end_time:
                        break
            else:
                if k>43212:
                    break
        fp.close()
    else:
        print("the file: " + dir + filename +" does not exist")
    return dict[date_index],dict[tps_index]


def makeDataFrame(dict,date_index,tps_index):
    tmp_dict = {date_index : dict[date_index], tps_index : dict[tps_index]}
    return pd.DataFrame(tmp_dict)

stats_dir = '/home/sramanan/scripts/OneNDS/ndsstats/'
txt_ext = '.txt'

bdsa_2_base_file_name = 'bdstor011_nlstats_'
bdsa_3_base_file_name = 'bdstor021_nlstats_'
bdsa_4_base_file_name = 'bdstor031_nlstats_' 
bdsa_5_base_file_name = 'bdstor041_nlstats_'
bdsa_6_base_file_name = 'bdstor051_nlstats_'
bdsa_7_base_file_name = 'bdstor061_nlstats_'

#FDS files.. convention 1 - 8 = toronto, 9 - 16 = montreal
fds_1_base_file_name = 'fdstor001_nlstats_'
fds_2_base_file_name = 'fdstor002_nlstats_'
fds_3_base_file_name = 'fdstor003_nlstats_'
fds_4_base_file_name = 'fdstor004_nlstats_'
fds_5_base_file_name = 'fdstor005_nlstats_'
fds_6_base_file_name = 'fdstor006_nlstats_'
fds_7_base_file_name = 'fdstor007_nlstats_'
fds_8_base_file_name = 'fdstor008_nlstats_'
fds_9_base_file_name = 'fdsmtl001_nlstats_'
fds_10_base_file_name = 'fdsmtl002_nlstats_'
fds_11_base_file_name = 'fdsmtl003_nlstats_'
fds_12_base_file_name = 'fdsmtl004_nlstats_'
fds_13_base_file_name = 'fdsmtl005_nlstats_'
fds_14_base_file_name = 'fdsmtl006_nlstats_'
fds_15_base_file_name = 'fdsmtl007_nlstats_'
fds_16_base_file_name = 'fdsmtl008_nlstats_'
email_address = sys.argv[3]

VIEW_BDS_GRAPH = sys.argv[6]
VIEW_FDS_GRAPH = sys.argv[7]

# #date 7 days ago - date today (yymmdd) (oldest date 2230 - newest date 2230)
DATE_CHOSEN = giveDate(int(sys.argv[4]),"Y","m","d","-")

#Time interval
START_TIME = sys.argv[1] 
END_TIME  = sys.argv[2] 
SAMPLE_INTERVAL = int(sys.argv[5])

#date array and time arrays used (always want to start with the date 1 day before the chosen date at 10:30PM, otherwise you could lose TPS info
date_arr = [giveDate(int(sys.argv[4])+1,"y","m","d",""),giveDate(int(sys.argv[4]),"y","m","d",""),giveDate(int(sys.argv[4])-1,"y","m","d","")]
date_arr_size = len(date_arr)
time_arr = ['1030','2230']



bdsa_data = {
    'bdsa2_date':[],
    'bdsa2_tps':[],
    'bdsa3_date':[],
    'bdsa3_tps':[],
    'bdsa4_date':[],
    'bdsa4_tps':[],
    'bdsa5_date':[],
    'bdsa5_tps':[],
    'bdsa6_date':[],
    'bdsa6_tps':[],
    'bdsa7_date':[],
    'bdsa7_tps':[]
}

fds_data = {
    'fds1_date':[],
    'fds1_tps':[],
    'fds2_date':[],
    'fds2_tps':[],
    'fds3_date':[],
    'fds3_tps':[],
    'fds4_date':[],
    'fds4_tps':[],
    'fds5_date':[],
    'fds5_tps':[],
    'fds6_date':[],
    'fds6_tps':[],
    'fds7_date':[],
    'fds7_tps':[],
    'fds8_date':[],
    'fds8_tps':[],
    'fds9_date':[],
    'fds9_tps':[],
    'fds10_date':[],
    'fds10_tps':[],
    'fds11_date':[],
    'fds11_tps':[],
    'fds12_date':[],
    'fds12_tps':[],
    'fds13_date':[],
    'fds13_tps':[],
    'fds14_date':[],
    'fds14_tps':[],
    'fds15_date':[],
    'fds15_tps':[],
    'fds16_date':[],
    'fds16_tps':[]
}


# variables to loop through date arr and time arr respectively
i = 0
j = 1

#os.system("cd " + stats_dir)
#loop through to gather all TPS data for DSAs 2 - 7 and store it in the data dictionary to send through Pandas
while(i<date_arr_size):
    #print("i is = " + str(i))
    #print("j is = " + str(j))
    bdsa_2_file_name = bdsa_2_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    bdsa_3_file_name = bdsa_3_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    bdsa_4_file_name = bdsa_4_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    bdsa_5_file_name = bdsa_5_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    bdsa_6_file_name = bdsa_6_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    bdsa_7_file_name = bdsa_7_base_file_name + date_arr[i] + time_arr[j] + txt_ext

    fds_1_file_name = fds_1_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_2_file_name = fds_2_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_3_file_name = fds_3_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_4_file_name = fds_4_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_5_file_name = fds_5_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_6_file_name = fds_6_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_7_file_name = fds_7_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_8_file_name = fds_8_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_9_file_name = fds_9_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_10_file_name = fds_10_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_11_file_name = fds_11_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_12_file_name = fds_12_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_13_file_name = fds_13_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_14_file_name = fds_14_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_15_file_name = fds_15_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    fds_16_file_name = fds_16_base_file_name + date_arr[i] + time_arr[j] + txt_ext
    
    #do logic here to read each file correctly, the parse correct info into the data dictionary
    #read each line as a string, then split by spaces, and take index = 2 (date) index = 3 (start time) index = 10,11,12,13,14 (TPS) 
    #10 = 10k-99k TPS, 11 = 1k - 9k TPS, 12 = 100-999 TPS, 13 = 10 - 99 TPS, 14 = 0 - 9 TPS
    #should be ploted as y (TPS) vs. x (start time (date) )
    
    #loop through each file 1 by 1 here...
    if VIEW_BDS_GRAPH == 'y':
        #get all stats for BDSA2
        bdsa_data['bdsa2_date'], bdsa_data['bdsa2_tps'] = getFileStats(stats_dir,bdsa_2_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa2_date','bdsa2_tps',"Updates Processed")
            
        #get all stats for BDSA3
        bdsa_data['bdsa3_date'], bdsa_data['bdsa3_tps'] = getFileStats(stats_dir,bdsa_3_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa3_date','bdsa3_tps',"Updates Processed")
            
        #get all stats for BDSA4
        bdsa_data['bdsa4_date'], bdsa_data['bdsa4_tps'] = getFileStats(stats_dir,bdsa_4_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa4_date','bdsa4_tps',"Updates Processed")
            
        #get all stats for BDSA5
        bdsa_data['bdsa5_date'], bdsa_data['bdsa5_tps'] = getFileStats(stats_dir,bdsa_5_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa5_date','bdsa5_tps',"Updates Processed")
            
        #get all stats for BDSA6
        bdsa_data['bdsa6_date'], bdsa_data['bdsa6_tps'] = getFileStats(stats_dir,bdsa_6_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa6_date','bdsa6_tps',"Updates Processed")
            
        #get all stats for BDSA7
        bdsa_data['bdsa7_date'], bdsa_data['bdsa7_tps'] = getFileStats(stats_dir,bdsa_7_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,bdsa_data,'bdsa7_date','bdsa7_tps',"Updates Processed")
     
    if VIEW_FDS_GRAPH == 'y':
        #get all stats for FDS1
        fds_data['fds1_date'], fds_data['fds1_tps'] = getFileStats(stats_dir,fds_1_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds1_date','fds1_tps',"Queries Processed")
            
        #get all stats for FDS2
        fds_data['fds2_date'], fds_data['fds2_tps'] = getFileStats(stats_dir,fds_2_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds2_date','fds2_tps',"Queries Processed")
            
        #get all stats for FDS3
        fds_data['fds3_date'], fds_data['fds3_tps'] = getFileStats(stats_dir,fds_3_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds3_date','fds3_tps',"Queries Processed")
            
        #get all stats for FDS4
        fds_data['fds4_date'], fds_data['fds4_tps'] = getFileStats(stats_dir,fds_4_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds4_date','fds4_tps',"Queries Processed")
            
        #get all stats for FDS5
        fds_data['fds5_date'], fds_data['fds5_tps'] = getFileStats(stats_dir,fds_5_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds5_date','fds5_tps',"Queries Processed")
            
        #get all stats for FDS6
        fds_data['fds6_date'], fds_data['fds6_tps'] = getFileStats(stats_dir,fds_6_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds6_date','fds6_tps',"Queries Processed")
            
        #get all stats for FDS7
        fds_data['fds7_date'], fds_data['fds7_tps'] = getFileStats(stats_dir,fds_7_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds7_date','fds7_tps',"Queries Processed")
            
        #get all stats for FDS8
        fds_data['fds8_date'], fds_data['fds8_tps'] = getFileStats(stats_dir,fds_8_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds8_date','fds8_tps',"Queries Processed")
            
        #get all stats for FDS9
        fds_data['fds9_date'], fds_data['fds9_tps'] = getFileStats(stats_dir,fds_9_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds9_date','fds9_tps',"Queries Processed")
            
        #get all stats for FDS10
        fds_data['fds10_date'], fds_data['fds10_tps'] = getFileStats(stats_dir,fds_10_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds10_date','fds10_tps',"Queries Processed")
            
        #get all stats for FDS11
        fds_data['fds11_date'], fds_data['fds11_tps'] = getFileStats(stats_dir,fds_11_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds11_date','fds11_tps',"Queries Processed")
            
        #get all stats for FDS12
        fds_data['fds12_date'], fds_data['fds12_tps'] = getFileStats(stats_dir,fds_12_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds12_date','fds12_tps',"Queries Processed")
            
        #get all stats for FDS13
        fds_data['fds13_date'], fds_data['fds13_tps'] = getFileStats(stats_dir,fds_13_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds13_date','fds13_tps',"Queries Processed")
            
        #get all stats for FDS14
        fds_data['fds14_date'], fds_data['fds14_tps'] = getFileStats(stats_dir,fds_14_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds14_date','fds14_tps',"Queries Processed")
            
        #get all stats for FDS15
        fds_data['fds15_date'], fds_data['fds15_tps'] = getFileStats(stats_dir,fds_15_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds15_date','fds15_tps',"Queries Processed")
            
        #get all stats for FDS16
        fds_data['fds16_date'], fds_data['fds16_tps'] = getFileStats(stats_dir,fds_16_file_name,DATE_CHOSEN,START_TIME,END_TIME,SAMPLE_INTERVAL,fds_data,'fds16_date','fds16_tps',"Queries Processed")
        
    #behavior at the end of each loop
    if(j == 1):
        i+=1
    j = 1 if j == 0 else 0

#BDS Graph/Excel processing
if VIEW_BDS_GRAPH == 'y':
    #make temporary dictionaries to create each individual data frame (i.e.: 1 dataframe per graph... 6 required)
    bdsa_2_data_df = makeDataFrame(bdsa_data,'bdsa2_date','bdsa2_tps')
    bdsa_3_data_df = makeDataFrame(bdsa_data,'bdsa3_date','bdsa3_tps')
    bdsa_4_data_df = makeDataFrame(bdsa_data,'bdsa4_date','bdsa4_tps')
    bdsa_5_data_df = makeDataFrame(bdsa_data,'bdsa5_date','bdsa5_tps')
    bdsa_6_data_df = makeDataFrame(bdsa_data,'bdsa6_date','bdsa6_tps')
    bdsa_7_data_df = makeDataFrame(bdsa_data,'bdsa7_date','bdsa7_tps')
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    bdsa_excel_file = 'OneNDS_BDSA_TPS_Report' + '-' + date_arr[1] + '.xlsx'
    bdsa_2_sheet_name = 'BDSA2 TPS'
    bdsa_3_sheet_name = 'BDSA3 TPS'
    bdsa_4_sheet_name = 'BDSA4 TPS'
    bdsa_5_sheet_name = 'BDSA5 TPS'
    bdsa_6_sheet_name = 'BDSA6 TPS'
    bdsa_7_sheet_name = 'BDSA7 TPS'
    
    #common writer for the same excel file (for all DSAs)
    writer_bdsa_file = pd.ExcelWriter(bdsa_excel_file, engine='xlsxwriter')
    
    #edit each sheet (for each DSA) individually
    
    bdsa_2_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_2_sheet_name)
    bdsa_3_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_3_sheet_name)
    bdsa_4_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_4_sheet_name)
    bdsa_5_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_5_sheet_name)
    bdsa_6_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_6_sheet_name)
    bdsa_7_data_df.to_excel(writer_bdsa_file, sheet_name=bdsa_7_sheet_name)
    
    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook_bdsa2 = writer_bdsa_file.book
    worksheet_bdsa2 = writer_bdsa_file.sheets[bdsa_2_sheet_name]
    
    workbook_bdsa3 = writer_bdsa_file.book
    worksheet_bdsa3 = writer_bdsa_file.sheets[bdsa_3_sheet_name]
    
    workbook_bdsa4 = writer_bdsa_file.book
    worksheet_bdsa4 = writer_bdsa_file.sheets[bdsa_4_sheet_name]
    
    workbook_bdsa5 = writer_bdsa_file.book
    worksheet_bdsa5 = writer_bdsa_file.sheets[bdsa_5_sheet_name]
    
    workbook_bdsa6 = writer_bdsa_file.book
    worksheet_bdsa6 = writer_bdsa_file.sheets[bdsa_6_sheet_name]
    
    workbook_bdsa7 = writer_bdsa_file.book
    worksheet_bdsa7 = writer_bdsa_file.sheets[bdsa_7_sheet_name]
    
    # Create a chart object.
    chart_bdsa2 = workbook_bdsa2.add_chart({'type': 'line'})
    chart_bdsa3 = workbook_bdsa3.add_chart({'type': 'line'})
    chart_bdsa4 = workbook_bdsa4.add_chart({'type': 'line'})
    chart_bdsa5 = workbook_bdsa5.add_chart({'type': 'line'})
    chart_bdsa6 = workbook_bdsa6.add_chart({'type': 'line'})
    chart_bdsa7 = workbook_bdsa7.add_chart({'type': 'line'})
    
    # Configure the series of the chart from the dataframe data.
    
    length_bdsa_2_tps_col = len(bdsa_data['bdsa2_date']) + 1
    length_bdsa_3_tps_col = len(bdsa_data['bdsa3_date']) + 1
    length_bdsa_4_tps_col = len(bdsa_data['bdsa4_date']) + 1
    length_bdsa_5_tps_col = len(bdsa_data['bdsa5_date']) + 1
    length_bdsa_6_tps_col = len(bdsa_data['bdsa6_date']) + 1
    length_bdsa_7_tps_col = len(bdsa_data['bdsa7_date']) + 1
    
    bdsa2_time_stat_col = '!$B$2:$B' + str(length_bdsa_2_tps_col)
    bdsa2_sheet_name_with_quotes = "'BDSA2 TPS'"
    bdsa2_tps_col = '='+bdsa2_sheet_name_with_quotes + bdsa2_time_stat_col
    
    
    bdsa3_time_stat_col = '!$B$2:$B' + str(length_bdsa_3_tps_col)
    bdsa3_sheet_name_with_quotes = "'BDSA3 TPS'"
    bdsa3_tps_col = '='+bdsa3_sheet_name_with_quotes + bdsa3_time_stat_col
    
    bdsa4_time_stat_col = '!$B$2:$B' + str(length_bdsa_4_tps_col)
    bdsa4_sheet_name_with_quotes = "'BDSA4 TPS'"
    bdsa4_tps_col = '='+bdsa4_sheet_name_with_quotes + bdsa4_time_stat_col
    
    bdsa5_time_stat_col = '!$B$2:$B' + str(length_bdsa_5_tps_col)
    bdsa5_sheet_name_with_quotes = "'BDSA5 TPS'"
    bdsa5_tps_col = '='+bdsa5_sheet_name_with_quotes + bdsa5_time_stat_col
    
    bdsa6_time_stat_col = '!$B$2:$B' + str(length_bdsa_6_tps_col)
    bdsa6_sheet_name_with_quotes = "'BDSA6 TPS'"
    bdsa6_tps_col = '='+bdsa6_sheet_name_with_quotes + bdsa6_time_stat_col
    
    bdsa7_time_stat_col = '!$B$2:$B' + str(length_bdsa_7_tps_col)
    bdsa7_sheet_name_with_quotes = "'BDSA7 TPS'"
    bdsa7_tps_col = '='+bdsa7_sheet_name_with_quotes + bdsa7_time_stat_col
    
    
    
    # categories = x axis (time), values = y-axis (TPS)
    chart_bdsa2.add_series({
        'categories': bdsa2_tps_col,
        'values': '=BDSA2 TPS!$C$2:$C'+ str(length_bdsa_2_tps_col)
    })
    
    
    chart_bdsa3.add_series({
        'categories': bdsa3_tps_col,
        'values': '=BDSA3 TPS!$C$2:$C'+ str(length_bdsa_3_tps_col)
    })
    
    chart_bdsa4.add_series({
        'categories': bdsa4_tps_col,
        'values': '=BDSA4 TPS!$C$2:$C'+ str(length_bdsa_4_tps_col)
    })
    
    chart_bdsa5.add_series({
        'categories': bdsa5_tps_col,
        'values': '=BDSA5 TPS!$C$2:$C'+ str(length_bdsa_5_tps_col)
    })
    
    chart_bdsa6.add_series({
        'categories': bdsa6_tps_col,
        'values': '=BDSA6 TPS!$C$2:$C'+ str(length_bdsa_6_tps_col)
    })
    
    chart_bdsa7.add_series({
        'categories': bdsa7_tps_col,
        'values': '=BDSA7 TPS!$C$2:$C'+ str(length_bdsa_7_tps_col)
    })
    
    # Configure the chart axes.
    chart_bdsa2.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa2.set_y_axis({'name': 'BDSA2 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa2.set_y_axis({'min': 2000, 'max': 6000})
    
    chart_bdsa3.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa3.set_y_axis({'name': 'BDSA3 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa3.set_y_axis({'min': 2000, 'max': 6000})
    
    chart_bdsa4.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa4.set_y_axis({'name': 'BDSA4 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa4.set_y_axis({'min': 2000, 'max': 6000})
    
    chart_bdsa5.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa5.set_y_axis({'name': 'BDSA5 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa5.set_y_axis({'min': 2000, 'max': 6000})
    
    chart_bdsa6.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa6.set_y_axis({'name': 'BDSA6 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa6.set_y_axis({'min': 2000, 'max': 8000})
    
    chart_bdsa7.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_bdsa7.set_y_axis({'name': 'BDSA7 TPS', 'major_gridlines': {'visible': False}})
    chart_bdsa7.set_y_axis({'min': 2000, 'max': 8000})
    
    # Turn off chart legend. It is on by default in Excel.
    chart_bdsa2.set_legend({'position': 'none'})
    chart_bdsa3.set_legend({'position': 'none'})
    chart_bdsa4.set_legend({'position': 'none'})
    chart_bdsa5.set_legend({'position': 'none'})
    chart_bdsa6.set_legend({'position': 'none'})
    chart_bdsa7.set_legend({'position': 'none'})
    
    # Insert the chart into the worksheet.
    worksheet_bdsa2.insert_chart('D2', chart_bdsa2, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_bdsa3.insert_chart('D2', chart_bdsa3, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_bdsa4.insert_chart('D2', chart_bdsa4, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_bdsa5.insert_chart('D2', chart_bdsa5, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_bdsa6.insert_chart('D2', chart_bdsa6, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_bdsa7.insert_chart('D2', chart_bdsa7, {'x_scale': 2.5, 'y_scale': 2.5})
    
    # Close the Pandas Excel writer and output the Excel file.
    writer_bdsa_file.save()
    
    
    
    
    mm = 'echo "" | mail -s "BDS TPS KPI report ' + giveDate(int(sys.argv[4]),"B","d","Y"," ") + '" ' + email_address + ' -A ' + bdsa_excel_file  + ' -r ' + 'sdm-reporter@bell.ca' 
    
    os.system(mm)



#FDS Graph/Excel processing
if VIEW_FDS_GRAPH == 'y':
    #make temporary dictionaries to create each individual data frame (i.e.: 1 dataframe per graph... 8 required)
    fds_1_data_df = makeDataFrame(fds_data,'fds1_date','fds1_tps')
    fds_2_data_df = makeDataFrame(fds_data,'fds2_date','fds2_tps')
    fds_3_data_df = makeDataFrame(fds_data,'fds3_date','fds3_tps')
    fds_4_data_df = makeDataFrame(fds_data,'fds4_date','fds4_tps')
    fds_5_data_df = makeDataFrame(fds_data,'fds5_date','fds5_tps')
    fds_6_data_df = makeDataFrame(fds_data,'fds6_date','fds6_tps')
    fds_7_data_df = makeDataFrame(fds_data,'fds7_date','fds7_tps')
    fds_8_data_df = makeDataFrame(fds_data,'fds8_date','fds8_tps')
    fds_9_data_df = makeDataFrame(fds_data,'fds9_date','fds9_tps')
    fds_10_data_df = makeDataFrame(fds_data,'fds10_date','fds10_tps')
    fds_11_data_df = makeDataFrame(fds_data,'fds11_date','fds11_tps')
    fds_12_data_df = makeDataFrame(fds_data,'fds12_date','fds12_tps')
    fds_13_data_df = makeDataFrame(fds_data,'fds13_date','fds13_tps')
    fds_14_data_df = makeDataFrame(fds_data,'fds14_date','fds14_tps')
    fds_15_data_df = makeDataFrame(fds_data,'fds15_date','fds15_tps')
    fds_16_data_df = makeDataFrame(fds_data,'fds16_date','fds16_tps')
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    fds_excel_file = 'OneNDS_FDS_TPS_Report' + '-' + date_arr[1] + '.xlsx'
    fds_1_sheet_name = 'FDSTOR001 TPS'
    fds_2_sheet_name = 'FDSTOR002 TPS'
    fds_3_sheet_name = 'FDSTOR003 TPS'
    fds_4_sheet_name = 'FDSTOR004 TPS'
    fds_5_sheet_name = 'FDSTOR005 TPS'
    fds_6_sheet_name = 'FDSTOR006 TPS'
    fds_7_sheet_name = 'FDSTOR007 TPS'
    fds_8_sheet_name = 'FDSTOR008 TPS'
    fds_9_sheet_name = 'FDSMTL001 TPS'
    fds_10_sheet_name = 'FDSMTL002 TPS'
    fds_11_sheet_name = 'FDSMTL003 TPS'
    fds_12_sheet_name = 'FDSMTL004 TPS'
    fds_13_sheet_name = 'FDSMTL005 TPS'
    fds_14_sheet_name = 'FDSMTL006 TPS'
    fds_15_sheet_name = 'FDSMTL007 TPS'
    fds_16_sheet_name = 'FDSMTL008 TPS'
    #common writer for the same excel file (for all FDS)
    writer_fds_file = pd.ExcelWriter(fds_excel_file, engine='xlsxwriter')
    
    #edit each sheet (for each FDS) individually
    fds_1_data_df.to_excel(writer_fds_file, sheet_name=fds_1_sheet_name)
    fds_2_data_df.to_excel(writer_fds_file, sheet_name=fds_2_sheet_name)
    fds_3_data_df.to_excel(writer_fds_file, sheet_name=fds_3_sheet_name)
    fds_4_data_df.to_excel(writer_fds_file, sheet_name=fds_4_sheet_name)
    fds_5_data_df.to_excel(writer_fds_file, sheet_name=fds_5_sheet_name)
    fds_6_data_df.to_excel(writer_fds_file, sheet_name=fds_6_sheet_name)
    fds_7_data_df.to_excel(writer_fds_file, sheet_name=fds_7_sheet_name)
    fds_8_data_df.to_excel(writer_fds_file, sheet_name=fds_8_sheet_name)
    fds_9_data_df.to_excel(writer_fds_file, sheet_name=fds_9_sheet_name)
    fds_10_data_df.to_excel(writer_fds_file, sheet_name=fds_10_sheet_name)
    fds_11_data_df.to_excel(writer_fds_file, sheet_name=fds_11_sheet_name)
    fds_12_data_df.to_excel(writer_fds_file, sheet_name=fds_12_sheet_name)
    fds_13_data_df.to_excel(writer_fds_file, sheet_name=fds_13_sheet_name)
    fds_14_data_df.to_excel(writer_fds_file, sheet_name=fds_14_sheet_name)
    fds_15_data_df.to_excel(writer_fds_file, sheet_name=fds_15_sheet_name)
    fds_16_data_df.to_excel(writer_fds_file, sheet_name=fds_16_sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook_fds1 = writer_fds_file.book
    worksheet_fds1 = writer_fds_file.sheets[fds_1_sheet_name]
    
    workbook_fds2 = writer_fds_file.book
    worksheet_fds2 = writer_fds_file.sheets[fds_2_sheet_name]
    
    workbook_fds3 = writer_fds_file.book
    worksheet_fds3 = writer_fds_file.sheets[fds_3_sheet_name]
    
    workbook_fds4 = writer_fds_file.book
    worksheet_fds4 = writer_fds_file.sheets[fds_4_sheet_name]
    
    workbook_fds5 = writer_fds_file.book
    worksheet_fds5 = writer_fds_file.sheets[fds_5_sheet_name]
    
    workbook_fds6 = writer_fds_file.book
    worksheet_fds6 = writer_fds_file.sheets[fds_6_sheet_name]
    
    workbook_fds7 = writer_fds_file.book
    worksheet_fds7 = writer_fds_file.sheets[fds_7_sheet_name]
    
    workbook_fds8 = writer_fds_file.book
    worksheet_fds8 = writer_fds_file.sheets[fds_8_sheet_name]
    
    workbook_fds9 = writer_fds_file.book
    worksheet_fds9 = writer_fds_file.sheets[fds_9_sheet_name]
    
    workbook_fds10 = writer_fds_file.book
    worksheet_fds10 = writer_fds_file.sheets[fds_10_sheet_name]
    
    workbook_fds11 = writer_fds_file.book
    worksheet_fds11 = writer_fds_file.sheets[fds_11_sheet_name]
    
    workbook_fds12 = writer_fds_file.book
    worksheet_fds12 = writer_fds_file.sheets[fds_12_sheet_name]
    
    workbook_fds13 = writer_fds_file.book
    worksheet_fds13 = writer_fds_file.sheets[fds_13_sheet_name]
    
    workbook_fds14 = writer_fds_file.book
    worksheet_fds14 = writer_fds_file.sheets[fds_14_sheet_name]
    
    workbook_fds15 = writer_fds_file.book
    worksheet_fds15 = writer_fds_file.sheets[fds_15_sheet_name]
    
    workbook_fds16 = writer_fds_file.book
    worksheet_fds16 = writer_fds_file.sheets[fds_16_sheet_name]
    
    # Create a chart object.
    chart_fds1 = workbook_fds1.add_chart({'type': 'line'})
    chart_fds2 = workbook_fds2.add_chart({'type': 'line'})
    chart_fds3 = workbook_fds3.add_chart({'type': 'line'})
    chart_fds4 = workbook_fds4.add_chart({'type': 'line'})
    chart_fds5 = workbook_fds5.add_chart({'type': 'line'})
    chart_fds6 = workbook_fds6.add_chart({'type': 'line'})
    chart_fds7 = workbook_fds7.add_chart({'type': 'line'})
    chart_fds8 = workbook_fds8.add_chart({'type': 'line'})
    chart_fds9 = workbook_fds9.add_chart({'type': 'line'})
    chart_fds10 = workbook_fds10.add_chart({'type': 'line'})
    chart_fds11 = workbook_fds11.add_chart({'type': 'line'})
    chart_fds12 = workbook_fds12.add_chart({'type': 'line'})
    chart_fds13 = workbook_fds13.add_chart({'type': 'line'})
    chart_fds14 = workbook_fds14.add_chart({'type': 'line'})
    chart_fds15 = workbook_fds15.add_chart({'type': 'line'})
    chart_fds16 = workbook_fds16.add_chart({'type': 'line'})
    
    # Configure the series of the chart from the dataframe data.
    
    length_fds_1_tps_col = len(fds_data['fds1_date']) + 1
    length_fds_2_tps_col = len(fds_data['fds2_date']) + 1
    length_fds_3_tps_col = len(fds_data['fds3_date']) + 1
    length_fds_4_tps_col = len(fds_data['fds4_date']) + 1
    length_fds_5_tps_col = len(fds_data['fds5_date']) + 1
    length_fds_6_tps_col = len(fds_data['fds6_date']) + 1
    length_fds_7_tps_col = len(fds_data['fds7_date']) + 1
    length_fds_8_tps_col = len(fds_data['fds8_date']) + 1
    length_fds_9_tps_col = len(fds_data['fds9_date']) + 1
    length_fds_10_tps_col = len(fds_data['fds10_date']) + 1
    length_fds_11_tps_col = len(fds_data['fds11_date']) + 1
    length_fds_12_tps_col = len(fds_data['fds12_date']) + 1
    length_fds_13_tps_col = len(fds_data['fds13_date']) + 1
    length_fds_14_tps_col = len(fds_data['fds14_date']) + 1
    length_fds_15_tps_col = len(fds_data['fds15_date']) + 1
    length_fds_16_tps_col = len(fds_data['fds16_date']) + 1
    
    fds1_time_stat_col = '!$B$2:$B' + str(length_fds_1_tps_col)
    fds1_sheet_name_with_quotes = "'FDSTOR001 TPS'"
    fds1_tps_col = '='+fds1_sheet_name_with_quotes + fds1_time_stat_col
    
    fds2_time_stat_col = '!$B$2:$B' + str(length_fds_2_tps_col)
    fds2_sheet_name_with_quotes = "'FDSTOR002 TPS'"
    fds2_tps_col = '='+fds2_sheet_name_with_quotes + fds2_time_stat_col
    
    
    fds3_time_stat_col = '!$B$2:$B' + str(length_fds_3_tps_col)
    fds3_sheet_name_with_quotes = "'FDSTOR003 TPS'"
    fds3_tps_col = '='+fds3_sheet_name_with_quotes + fds3_time_stat_col
    
    fds4_time_stat_col = '!$B$2:$B' + str(length_fds_4_tps_col)
    fds4_sheet_name_with_quotes = "'FDSTOR004 TPS'"
    fds4_tps_col = '='+fds4_sheet_name_with_quotes + fds4_time_stat_col
    
    fds5_time_stat_col = '!$B$2:$B' + str(length_fds_5_tps_col)
    fds5_sheet_name_with_quotes = "'FDSTOR005 TPS'"
    fds5_tps_col = '='+fds5_sheet_name_with_quotes + fds5_time_stat_col
    
    fds6_time_stat_col = '!$B$2:$B' + str(length_fds_6_tps_col)
    fds6_sheet_name_with_quotes = "'FDSTOR006 TPS'"
    fds6_tps_col = '='+fds6_sheet_name_with_quotes + fds6_time_stat_col
    
    fds7_time_stat_col = '!$B$2:$B' + str(length_fds_7_tps_col)
    fds7_sheet_name_with_quotes = "'FDSTOR007 TPS'"
    fds7_tps_col = '='+fds7_sheet_name_with_quotes + fds7_time_stat_col
    
    fds8_time_stat_col = '!$B$2:$B' + str(length_fds_8_tps_col)
    fds8_sheet_name_with_quotes = "'FDSTOR008 TPS'"
    fds8_tps_col = '='+fds8_sheet_name_with_quotes + fds8_time_stat_col
    
    fds9_time_stat_col = '!$B$2:$B' + str(length_fds_9_tps_col)
    fds9_sheet_name_with_quotes = "'FDSMTL001 TPS'"
    fds9_tps_col = '='+fds9_sheet_name_with_quotes + fds9_time_stat_col
    
    fds10_time_stat_col = '!$B$2:$B' + str(length_fds_10_tps_col)
    fds10_sheet_name_with_quotes = "'FDSMTL002 TPS'"
    fds10_tps_col = '='+fds10_sheet_name_with_quotes + fds10_time_stat_col
    
    fds11_time_stat_col = '!$B$2:$B' + str(length_fds_11_tps_col)
    fds11_sheet_name_with_quotes = "'FDSMTL003 TPS'"
    fds11_tps_col = '='+fds11_sheet_name_with_quotes + fds11_time_stat_col
    
    fds12_time_stat_col = '!$B$2:$B' + str(length_fds_12_tps_col)
    fds12_sheet_name_with_quotes = "'FDSMTL004 TPS'"
    fds12_tps_col = '='+fds12_sheet_name_with_quotes + fds12_time_stat_col
    
    fds13_time_stat_col = '!$B$2:$B' + str(length_fds_13_tps_col)
    fds13_sheet_name_with_quotes = "'FDSMTL005 TPS'"
    fds13_tps_col = '='+fds13_sheet_name_with_quotes + fds13_time_stat_col
    
    fds14_time_stat_col = '!$B$2:$B' + str(length_fds_14_tps_col)
    fds14_sheet_name_with_quotes = "'FDSMTL006 TPS'"
    fds14_tps_col = '='+fds14_sheet_name_with_quotes + fds14_time_stat_col
    
    fds15_time_stat_col = '!$B$2:$B' + str(length_fds_15_tps_col)
    fds15_sheet_name_with_quotes = "'FDSMTL007 TPS'"
    fds15_tps_col = '='+fds15_sheet_name_with_quotes + fds15_time_stat_col
    
    fds16_time_stat_col = '!$B$2:$B' + str(length_fds_16_tps_col)
    fds16_sheet_name_with_quotes = "'FDSMTL008 TPS'"
    fds16_tps_col = '='+fds16_sheet_name_with_quotes + fds16_time_stat_col

    # categories = x axis (time), values = y-axis (TPS)
    
    chart_fds1.add_series({
        'categories': fds1_tps_col,
        'values': '=FDSTOR001 TPS!$C$2:$C'+ str(length_fds_1_tps_col)
    })
    
    chart_fds2.add_series({
        'categories': fds2_tps_col,
        'values': '=FDSTOR002 TPS!$C$2:$C'+ str(length_fds_2_tps_col)
    })
    
    
    chart_fds3.add_series({
        'categories': fds3_tps_col,
        'values': '=FDSTOR003 TPS!$C$2:$C'+ str(length_fds_3_tps_col)
    })
    
    chart_fds4.add_series({
        'categories': fds4_tps_col,
        'values': '=FDSTOR004 TPS!$C$2:$C'+ str(length_fds_4_tps_col)
    })
    
    chart_fds5.add_series({
        'categories': fds5_tps_col,
        'values': '=FDSTOR005 TPS!$C$2:$C'+ str(length_fds_5_tps_col)
    })
    
    chart_fds6.add_series({
        'categories': fds6_tps_col,
        'values': '=FDSTOR006 TPS!$C$2:$C'+ str(length_fds_6_tps_col)
    })
    
    chart_fds7.add_series({
        'categories': fds7_tps_col,
        'values': '=FDSTOR007 TPS!$C$2:$C'+ str(length_fds_7_tps_col)
    })
    
    chart_fds8.add_series({
        'categories': fds8_tps_col,
        'values': '=FDSTOR008 TPS!$C$2:$C'+ str(length_fds_8_tps_col)
    })
    
    chart_fds9.add_series({
        'categories': fds9_tps_col,
        'values': '=FDSMTL001 TPS!$C$2:$C'+ str(length_fds_9_tps_col)
    })
    
    chart_fds10.add_series({
        'categories': fds10_tps_col,
        'values': '=FDSMTL002 TPS!$C$2:$C'+ str(length_fds_10_tps_col)
    })
    
    chart_fds11.add_series({
        'categories': fds11_tps_col,
        'values': '=FDSMTL003 TPS!$C$2:$C'+ str(length_fds_11_tps_col)
    })
    
    chart_fds12.add_series({
        'categories': fds12_tps_col,
        'values': '=FDSMTL004 TPS!$C$2:$C'+ str(length_fds_12_tps_col)
    })
    
    chart_fds13.add_series({
        'categories': fds13_tps_col,
        'values': '=FDSMTL005 TPS!$C$2:$C'+ str(length_fds_13_tps_col)
    })
    
    chart_fds14.add_series({
        'categories': fds14_tps_col,
        'values': '=FDSMTL006 TPS!$C$2:$C'+ str(length_fds_14_tps_col)
    })
    
    chart_fds15.add_series({
        'categories': fds15_tps_col,
        'values': '=FDSMTL007 TPS!$C$2:$C'+ str(length_fds_15_tps_col)
    })
    
    chart_fds16.add_series({
        'categories': fds16_tps_col,
        'values': '=FDSMTL008 TPS!$C$2:$C'+ str(length_fds_16_tps_col)
    })
    
    # Configure the chart axes.
    chart_fds1.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds1.set_y_axis({'name': 'FDSTOR001 TPS', 'major_gridlines': {'visible': False}})
    chart_fds1.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds2.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds2.set_y_axis({'name': 'FDSTOR002 TPS', 'major_gridlines': {'visible': False}})
    chart_fds2.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds3.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds3.set_y_axis({'name': 'FDSTOR003 TPS', 'major_gridlines': {'visible': False}})
    chart_fds3.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds4.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds4.set_y_axis({'name': 'FDSTOR004 TPS', 'major_gridlines': {'visible': False}})
    chart_fds4.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds5.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds5.set_y_axis({'name': 'FDSTOR005 TPS', 'major_gridlines': {'visible': False}})
    chart_fds5.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds6.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds6.set_y_axis({'name': 'FDSTOR006 TPS', 'major_gridlines': {'visible': False}})
    chart_fds6.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds7.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds7.set_y_axis({'name': 'FDSTOR007 TPS', 'major_gridlines': {'visible': False}})
    chart_fds7.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds8.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds8.set_y_axis({'name': 'FDSTOR008 TPS', 'major_gridlines': {'visible': False}})
    chart_fds8.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds9.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds9.set_y_axis({'name': 'FDSMTL001 TPS', 'major_gridlines': {'visible': False}})
    chart_fds9.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds10.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds10.set_y_axis({'name': 'FDSMTL002 TPS', 'major_gridlines': {'visible': False}})
    chart_fds10.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds11.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds11.set_y_axis({'name': 'FDSMTL003 TPS', 'major_gridlines': {'visible': False}})
    chart_fds11.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds12.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds12.set_y_axis({'name': 'FDSMTL004 TPS', 'major_gridlines': {'visible': False}})
    chart_fds12.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds13.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds13.set_y_axis({'name': 'FDSMTL005 TPS', 'major_gridlines': {'visible': False}})
    chart_fds13.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds14.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds14.set_y_axis({'name': 'FDSMTL006 TPS', 'major_gridlines': {'visible': False}})
    chart_fds14.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds15.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds15.set_y_axis({'name': 'FDSMTL007 TPS', 'major_gridlines': {'visible': False}})
    chart_fds15.set_y_axis({'min': 1000, 'max': 8000})
    
    chart_fds16.set_x_axis({'name': 'time (date)', 'position_axis': 'on_tick'})
    chart_fds16.set_y_axis({'name': 'FDSMTL008 TPS', 'major_gridlines': {'visible': False}})
    chart_fds16.set_y_axis({'min': 1000, 'max': 8000})
    
    # Turn off chart legend. It is on by default in Excel.
    chart_fds1.set_legend({'position': 'none'})
    chart_fds2.set_legend({'position': 'none'})
    chart_fds3.set_legend({'position': 'none'})
    chart_fds4.set_legend({'position': 'none'})
    chart_fds5.set_legend({'position': 'none'})
    chart_fds6.set_legend({'position': 'none'})
    chart_fds7.set_legend({'position': 'none'})
    chart_fds8.set_legend({'position': 'none'})
    chart_fds9.set_legend({'position': 'none'})
    chart_fds10.set_legend({'position': 'none'})
    chart_fds11.set_legend({'position': 'none'})
    chart_fds12.set_legend({'position': 'none'})
    chart_fds13.set_legend({'position': 'none'})
    chart_fds14.set_legend({'position': 'none'})
    chart_fds15.set_legend({'position': 'none'})
    chart_fds16.set_legend({'position': 'none'})
    
    # Insert the chart into the worksheet.
    worksheet_fds1.insert_chart('D2', chart_fds1, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds2.insert_chart('D2', chart_fds2, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds3.insert_chart('D2', chart_fds3, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds4.insert_chart('D2', chart_fds4, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds5.insert_chart('D2', chart_fds5, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds6.insert_chart('D2', chart_fds6, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds7.insert_chart('D2', chart_fds7, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds8.insert_chart('D2', chart_fds8, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds9.insert_chart('D2', chart_fds9, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds10.insert_chart('D2', chart_fds10, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds11.insert_chart('D2', chart_fds11, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds12.insert_chart('D2', chart_fds12, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds13.insert_chart('D2', chart_fds13, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds14.insert_chart('D2', chart_fds14, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds15.insert_chart('D2', chart_fds15, {'x_scale': 2.5, 'y_scale': 2.5})
    worksheet_fds16.insert_chart('D2', chart_fds16, {'x_scale': 2.5, 'y_scale': 2.5})
    
    # Close the Pandas Excel writer and output the Excel file.
    writer_fds_file.save()
    
    
    
    
    mm = 'echo "" | mail -s "FDS TPS KPI report ' + giveDate(int(sys.argv[4]),"B","d","Y"," ") + '" ' + email_address + ' -A ' + fds_excel_file  + ' -r ' + 'sdm-reporter@bell.ca' 
    
    os.system(mm)
# print(data['bdsa2_date'][0])
# print(data['bdsa2_tps'][0])
# print(data['bdsa2_date'][len(data['bdsa2_date'])-1])
# print(data['bdsa2_tps'][len(data['bdsa2_tps'])-1])

# print(data['bdsa3_date'][0])
# print(data['bdsa3_tps'][0])
# print(data['bdsa3_date'][len(data['bdsa3_date'])-1])
# print(data['bdsa3_tps'][len(data['bdsa3_tps'])-1])

# print(data['bdsa4_date'][0])
# print(data['bdsa4_tps'][0])
# print(data['bdsa4_date'][len(data['bdsa4_date'])-1])
# print(data['bdsa4_tps'][len(data['bdsa4_tps'])-1])

# print(data['bdsa5_date'][0])
# print(data['bdsa5_tps'][0])
# print(data['bdsa5_date'][len(data['bdsa5_date'])-1])
# print(data['bdsa5_tps'][len(data['bdsa5_tps'])-1])

# print(data['bdsa6_date'][0])
# print(data['bdsa6_tps'][0])
# print(data['bdsa6_date'][len(data['bdsa6_date'])-1])
# print(data['bdsa6_tps'][len(data['bdsa6_tps'])-1])

# print(data['bdsa7_date'][0])
# print(data['bdsa7_tps'][0])
# print(data['bdsa7_date'][len(data['bdsa7_date'])-1])
# print(data['bdsa7_tps'][len(data['bdsa7_tps'])-1])


# 13 files per dsa
#only read lines 13 - 43212 from each file (where the data is)