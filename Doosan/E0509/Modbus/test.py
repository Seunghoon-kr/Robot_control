robot_action_dic = {'robot_off' : {
                        'current_state' : [0,0,0,0,0],
                        'next_action' : ['power_on', [0, True]]
                        },
                    'robot_on' : {
                        'current_state' : [3,0,0,0,0],
                        'next_action' : ['script_start',[1,False]]
                        },
                    'robot_running' : {
                        'current_state' : [3,1,1,0,0],
                        'next_action' : ['manual_on',[2,True]]
                        },
                    'ss2' : {
                        'current_state' : [5,3,3,0,0],
                        'next_action' : ['error_off',[3,False]]
                        }
                    }

target_state = [3,1,1,0,0]
matching_keys = [key for key, value in robot_action_dic.items() if value['current_state'] == target_state]
for key in matching_keys:
    print(key)
print(robot_action_dic[key]['next_action'][1])