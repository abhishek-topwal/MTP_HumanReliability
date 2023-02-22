#lists for storing the activity of every event
sysmon_list = []
track_list = []
comm_list = []



def getSysmonScore(sysmon_list):
    total_failures = 0
    total_hits = 0
    response_time = 0

    for i,event in sysmon_list:
        if event[5] == 'FAILURE\n':
            total_failures += 1
            if(sysmon_list[i+1][5]=='HIT\n'):


        if event[3] == 'Success':
            total_hits += 1 
    print(total_failures)

if __name__ == '__main__':
    participant_info = []


    # get path of log file
    log_file_path = 'Logs/complete_sysmon_20230222_1513.log'

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

getSysmonScore(sysmon_list)
