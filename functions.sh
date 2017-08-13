#!/usr/bin/env bash
# Here you can create functions which will be available from the commands file
# You can also use here user variables defined in your config file
# To avoid conflicts, name your function like this
# jv_pg_XX_myfunction () { }
# jv for JarVis
# pg for PluGin
# XX can be a two letters code for your plugin, ex: ww for Weather Wunderground

jv_pg_api_start () {
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    jv_debug "Starting RestAPI server on http://$jv_ip:$jv_pg_api_port"
    python2 $DIR/server.py --port $jv_pg_api_port --key "$jv_pg_api_key" & # 2>&1 | jv_add_timestamps >>$jv_dir/jarvis.log &
}
