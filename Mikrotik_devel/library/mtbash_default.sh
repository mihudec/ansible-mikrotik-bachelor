#!/usr/bin/expect


#Destination MAC Address
set mac [lindex $argv 0]
#Username used for connection
set user [lindex $argv 1]
#Password used for connection
set pass [lindex $argv 2]
#Set Mikrotik's Identity
set identity [lindex $argv 3]
#Username for new user
set new_user [lindex $argv 4]
#Password for new user
set new_pass [lindex $argv 5]
#Interface used for management
set interface [lindex $argv 6]
#IP address used for management
set ip [lindex $argv 7]



set ses 1
set $::env(TERM) xterm
spawn "mactelnet" "$mac"
set ses $spawn_id
set timeout 200
expect -i $ses "Login:"
exp_send -i $ses "$user\r"
expect -i $ses "Password:"
exp_send -i $ses "$pass\r"
sleep 5
exp_send -i $ses "\r"


#Set identity
expect -i $ses "*>*"
exp_send -i $ses "/system identity set name=$identity\r"
sleep 1

#Create new user for management
expect -i $ses "*>*"
exp_send -i $ses "/user add name=$new_user password=$new_pass group=full\r"
sleep 1

#Set IP address on connected interface
expect -i $ses "*>*"
exp_send -i $ses "/ip address add address=$ip interface=$interface\r"
sleep 1

#END
expect -i $ses "*>*"
exp_send -i $ses "^D"
exit
