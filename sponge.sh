#!/bin/bash
#
# chkconfig: 35 90 12
# description: Sponge Runner
#
# Get function from functions library
. /etc/init.d/functions

# Start
start() {
    if running $1;
    then
        echo "Sponge Already Running"
        echo;
    else
        echo "Starting Sponge Server..."
        sudo python /home/ec2-user/sponge/app.py -c /home/ec2-user/sponge.json > /dev/null 2>&1 &
        ### Create the lock file ###
        touch /var/lock/subsys/sponge
        echo "Sponge Running"
        echo;
    fi
}

# Restart
stop() {
    if running $1;
    then
        echo "Stopping Sponge Server..."
        ps -aef | grep "sudo python /home/ec2-user/sponge/app.py" | awk '{print $2}' | xargs sudo kill > /dev/null 2>&1 &
        ### Remove the Lock File ###
        rm -f /var/lock/subsys/sponge
        echo "Sponge Stopped"
        echo;
    else
        echo "Sponge Not Running"
        echo;
    fi
}
# Status
status() {
    if running $1;
    then
        echo "Sponge Running"
        echo;
    else
        echo "Sponge Not Running"
        echo;
    fi
}

running() {
    if [ -f "/var/lock/subsys/sponge" ]
    then
        return 0
    else
        return 1
    fi
}

### main logic ###
"sponge" 80L, 1484C
