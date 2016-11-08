#!/bin/bash
# Here you can create functions which will be available from the commands file
# You can also use here user variables defined in your config file
# To avoid conflicts, name your function like this
# jv_pg_XX_myfunction () { }
# jv for JarVis
# pg for PluGin
# XX can be a two letters code for your plugin, ex: ww for Weather Wunderground

jv_pg_api_myip () {
    ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'
}

jv_pg_api_start () {
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    jv_debug "Starting RestAPI server on http://$(jv_pg_api_myip):$jv_pg_api_port"
    python $DIR/../server.py --port $jv_pg_api_port &
}

# do not start http server if just executing an order
[ "$just_execute" == false ] && jv_pg_api_start
