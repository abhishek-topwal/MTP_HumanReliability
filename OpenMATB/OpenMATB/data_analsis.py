 # opne the data.txt file

# eeg and pulse data in format timestamp : value
from datetime import datetime
from pathlib import Path
eeg_data = {}
pulse_data = {}

j = 0
with open('data.txt', 'r') as f:
    #read each line
    for line in f:
        #split the line into a list
        line = line.split('||')
        # get type, timestamp and data
        type = line[0].strip()

        timestamps = line[1].replace('[','').replace(']','').replace(' ','').split(',')

        data = line[2].split('], [')
        for i in range(len(data)):
            data[i] = data[i].replace('[','').replace(']','').replace(' ','')

        if(type=="EEG"):
            for i in range(len(timestamps)):
                # print(timestamps[i], data[i])
                # convert timestamp to float
                #

                timestamps[i] = float(timestamps[i])
                time = datetime.fromtimestamp(timestamps[i])
                j+=1

                print('====================================')
                print(time)
                print(timestamps[i])
                eeg_data[timestamps[i]] = data[i]
                print('====================================')

        if(type=="Pulse"):
            for i in range(len(timestamps)):
                # print(timestamps[i], data[i])
                pulse_data[timestamps[i]] = data[i]


# print(eeg_data)

# i = 0
# log_file_dir = Path('Logs')
# log_file_path = log_file_dir / 'scenario_settings5_20230309_1032.log'
# print('====================================')
# print('====================================')
# print('====================================')
# with open(log_file_path, 'r') as file:
#     for line in file:
#         line = line.split('\t')
#         if(len(line)<=3):
#             continue
#         i+=1

#         day = str(datetime.now()).split(' ')[0]
#         time = datetime.strptime(day+' '+str(line[0]), '%Y-%m-%d %H:%M:%S.%f')
#         #convert time to timestamp

#         time = time.timestamp()
#         print(time)

#         if(i==50):
#             break


