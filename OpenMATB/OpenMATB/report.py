#lists for storing the activity of every event
sysmon_list = []
track_list = []
comm_list = []


if __name__ == '__main__':
    participant_info = []


    # get path of log file
    log_file_path = 'Logs/scenario_settings1_20230219_1833.log'

    # #open a file
    # f = open(log_file_path, 'w')

    # traverse thorugh the log file
    with open(log_file_path ,'r') as f:
        for line in f:
            line = line.split('\t')

            if(len(line)<=1):
                continue
            
            if line[2] == 'SYSMON':
                sysmon_list.append(line)

print(sysmon_list)         

