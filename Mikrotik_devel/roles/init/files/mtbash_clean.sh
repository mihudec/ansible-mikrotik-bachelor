#!/usr/bin/expect


set mac [lindex $argv 0]
set user [lindex $argv 1]
set pass [lindex $argv 2]

#Init phase
set ses 1

set $::env(TERM) xterm
spawn "mactelnet" "$mac"
set ses $spawn_id
set timeout 200
expect -i $ses "Login:"
send -i $ses "$user\r"
expect -i $ses "Password:"
send -i $ses "$pass\r"
sleep 5
send -i $ses "\r"


#Reset configuration with no default settings
expect "*>*"
send -i $ses "/system reset-configuration no-defaults=yes\r"
sleep 1
send -i $ses "y\r"
sleep 1

exit 0

