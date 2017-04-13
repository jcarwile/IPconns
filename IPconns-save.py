import os
import platform

''' #!/bin/env python '''


def conns_command():
    cmd = 'onetstat'
    c = os.popen(cmd)
    cmd_array = []
    for line in c.readline():
        if 'NETSTAT' in line:
            continue
        elif 'User Id' in line:
            continue
        elif '-----' in line:
            continue
        else:
            sline = line.rstrip()
            cmd_array.append(sline)
    return cmd_array


def conns_file():
    file_path = '/home/jcarwile/python/IPconns/IPconns.txt'
    f = open(file_path, 'r')
    file_array = []
    for line in f.readlines():
        if 'NETSTAT' in line:
            continue
        elif 'User Id' in line:
            continue
        elif '-----' in line:
            continue
        else:
            sline = line.rstrip()
            file_array.append(sline)
    return file_array


def get_conns_array():
    platfm = platform.system()
    if platfm == 'OS/390':
        print 'This is the mainframe'
        conn_array = conns_command()
    else:
        print 'This is Linux'
        conn_array = conns_file()
    return conn_array


def total_rem_conns_by_user(e_array):
    tn3270_cnt = other_cnt = 0
    tot_array = [ ['AAAAAA 999 1.1.1.1', 0], ['BBBBB 999 2.2.2.2', 0] ]
    for item in e_array:      # user, loc_ip, loc_port, rem_ip, rem_port, state
        if item[0] == 'TN3270':
            tn3270_cnt += 1
        else:
            other_cnt += 1
        name_port_remip =  str(item[0] + ' ' + str(item[2]) + ' ' + str(item[3]))
        notfound_sw = True
        for ent in tot_array:
            if name_port_remip == ent[0]:
                notfound_sw = False
                index = tot_array.index(ent)
                new_cnt = tot_array[index][1] + 1
                tot_array[index][1] = new_cnt
        if notfound_sw:
            new_entry = [name_port_remip, 1]
            tot_array.append(new_entry)

    print 'Total TN3270 connections:', tn3270_cnt
    print 'Total Other connections: ', other_cnt
    print 'Total number of Established connections:', tn3270_cnt + other_cnt

    return tot_array


if __name__ == '__main__':
    conn_lines = get_conns_array()
    print 'This is the array of connections:'
    Listen_conns = []
    Establish_conns = []
    Internal_conns = []
    Other_conns = []

    for conn_line in conn_lines:
        user, connid, loc_sock, rem_sock, state = conn_line.split()
        loc_ip, loc_port = loc_sock.split('..')
        rem_ip, rem_port = rem_sock.split('..')
        tmp_array = [user, loc_ip, loc_port, rem_ip, rem_port, state]
        if 'Listen' in conn_line:
            Listen_conns.append(tmp_array)
        elif 'Establsh' in conn_line:
            if loc_ip == '127.0.0.1':
                Internal_conns.append(tmp_array)
            else:
                Establish_conns.append(tmp_array)
        else:
            Other_conns.append(tmp_array)

    tot_cnt = 0

    tmp_cnt = 0
    print 'This is the list of Listening ports'
    for item in Listen_conns:
        user = item[0]
        loc_port = item[2]
        print user, loc_port
        tmp_cnt += 1
    print 'Total Listening ports', tmp_cnt
    tot_cnt += tmp_cnt

    tmp_cnt = 0
    print '\n\nThis is the list of Internal connections'
    for item in Internal_conns:
        user = item[0]
        loc_port = item[2]
        state = item[5]
        print user, loc_port, state
        tmp_cnt += 1
    print 'Total Internal connections', tmp_cnt
    tot_cnt += tmp_cnt

    tmp_cnt = 0
    print '\n\nThis is the list of Other connection states'
    for item in Other_conns:
        user = item[0]
        loc_port = item[2]
        rem_ip = item[3]
        rem_port = item[4]
        state = item[5]
        print user, loc_port, rem_ip, rem_port, state
        tmp_cnt += 1
    print 'Total Other connections'
    tot_cnt += tmp_cnt

    print '\n\nTotal of all non-Established connections', tot_cnt

    t_array = total_rem_conns_by_user(Establish_conns)
    print '\n\nThis is the list of Established connections with count greater than 1'
    print '{0:8}   {1:5}   {2:15}   {3:5}'.format('Name', 'Port', 'Remote IP', 'Count')
    print '{0:8}   {1:5}   {2:15}   {3:5}'.format('------', '----', '---------------', '---')
    calc_tn3270_cnt = 0
    for item in t_array:
        calc_tn3270_cnt += item[1]
        if item[1] > 1:
            user, port, ip = item[0].split()
            print '{0:8}   {1:5}   {2:18}   {3:5d}'.format(user, port, ip, item[1])

    print 'The total number of calculated Established connections:', calc_tn3270_cnt

