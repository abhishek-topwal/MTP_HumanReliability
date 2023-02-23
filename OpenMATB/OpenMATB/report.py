from datetime import datetime

#lists for storing the activity of every event
sysmon_list = []
track_list = []
comm_list = []

def getCommScore(comm_list):

    curr_target = ''
    response_times = []
    repsonse_accuracies = []
    for i in range(len(comm_list)):
        if comm_list[i][4]=='OWN' and comm_list[i][6]=='TARGET':
            #get tht channel
            channel = comm_list[i][5]
            #get the start time
            start_time = datetime.strptime(comm_list[i][0], '%H:%M:%S.%f')
            #get the current target
            curr_target = comm_list[i][7].strip()

            #traverse till the subject press enter
            #check for enter press and compare with the last entered frequency

            # flag to check whether 'ENTER' is pressed
            flag = 0
            j = i
            while comm_list[j][5]!='RETURN':
                j+=1
                if(j==len(comm_list)-1) or comm_list[j][4]=='OWN' and comm_list[j][6]=='TARGET':
                    flag = 1
                    break

            if(flag==1):
                # case when 'ENTER' is not pressed and another prompt has started
                # add 30 seconds to the response time
                response_times.append(30)
                # add 0 to the accuracy
                repsonse_accuracies.append(0)
                i=j
                continue

            #case when 'ENTER' is pressed
            i=j
            while not (comm_list[j][4]=='OWN' and comm_list[j][5]==channel):
                j-=1

            end_time = datetime.strptime(comm_list[i][0], '%H:%M:%S.%f')
            response_time = end_time - start_time
            # print(response_time.total_seconds())
            response_times.append(response_time.total_seconds())
            #get the accuracy
            last_freq = float(comm_list[j][6].strip())
            print(f'curent target:{curr_target} last frequency:{last_freq}')
            error = abs(float(curr_target) - float(comm_list[j][6].strip()))/float(curr_target)
            # print(error)
            accuracy = 1 - error
            repsonse_accuracies.append(accuracy) 

    print('Response Times: ',response_times)
    print('Response Accuracies: ',repsonse_accuracies)


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
    log_file_path = 'Logs/complete_comm_20230223_1607.log'

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
            
            if line[2] == 'COMMUN':
                comm_list.append(line)


# [print (i) for i in comm_list]

getCommScore(comm_list)
# getSysmonScore(sysmon_list)
