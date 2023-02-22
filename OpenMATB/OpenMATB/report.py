from datetime import datetime

#lists for storing the activity of every event
sysmon_list = []
track_list = []
comm_list = []



def getSysmonScore(sysmon_list):
    total_failures = 0
    total_hits = 0
    false_alarm = 0
    response_time = 0

    for i,event in enumerate(sysmon_list)   :
        if event[5] == 'FAILURE\n':
            total_failures += 1
            #check if the next event is a hit
            if(sysmon_list[i+1][5]=='HIT\n'):
                total_hits += 1

            #check if the next event is a miss 
            if(sysmon_list[i+1][5]=='MISS\n'):
                false_alarm += 1

            #calculate response time
            time1 = datetime.strptime(sysmon_list[i][0], '%H:%M:%S.%f')
            time2 = datetime.strptime(sysmon_list[i+1][0], '%H:%M:%S.%f')                
            res = time2 - time1
            print(res.total_seconds())
            response_time += res.total_seconds()

    avg_response_time = response_time/total_failures;
    print('Total Failures: ',total_failures)
    print('Total Hits: ',total_hits)
    print('False Alarms: ',false_alarm)
    print('Average Response Time: ',avg_response_time)


if __name__ == '__main__':
    participant_info = []


    # get path of log file
    log_file_path = 'Logs/complete_sysmon_20230222_1708.log'

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

# print(sysmon_list)
getSysmonScore(sysmon_list)
