def _create_date(raw_data):
    date =  list(str(raw_data))
    return str(date[0])+str(date[1]) + '.' + str(date[2])+str(date[3]) + '.' + str(date[4])+str(date[5])

def _create_time(raw_data):
    time = list(str(raw_data))
    return str(int(str(time[0])+str(time[1])) + 3) + ':' + str(time[2])+str(time[3]) + ':' + str(time[4])+str(time[5])

def save_to_file(type_ts, gps_message_list):
    file = open(f'{type_ts}.txt', 'w', encoding="utf-8")        
    file.write(str(gps_message_list))

def save_to_json(type_ts, date, time, Longitude, Latitude, status):
    import json
    with open('data.json') as json_file:
        data = json.load(json_file)
    
    data.update({str(type_ts): 
                {'Date':str(date),
                'Time':str(time),
                'Longitude':str(Longitude),
                'Latitude':str(Latitude),
                'status':str(status)}}
            )
    with open('data.json', 'w') as outfile:
        outfile.write(json.dumps(data))
