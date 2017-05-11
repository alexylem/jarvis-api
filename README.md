<!---
IMPORTANT
=========
This README.md is displayed in the WebStore as well as within Jarvis app
Please do not change the structure of this file
Fill-in Description, Usage & Author sections
Make sure to rename the [en] folder into the language code your plugin is written in (ex: fr, es, de, it...)
For multi-language plugin:
- clone the language directory and translate commands/functions.sh
- optionally write the Description / Usage sections in several languages
-->
## Description
This plugin embeds a lightweight RestAPI server to control Jarvis remotely.
The HTTP Server is based on Python, so no dependency to install.
There is no configuration needed, just install the plugin and start Jarvis normally.

## Usage
```
$> jarvis
Starting RestAPI server on http://192.168.1.20:8080
Jarvis: Bonjour Alex
...
```
Now you can control Jarvis from another device.

From a browser, simply type in the URL to make Jarvis say something:
```
http://192.168.1.20:8080?say=Hello World
```
![image](https://cloud.githubusercontent.com/assets/11017174/25438915/26d18d8a-2a9b-11e7-98b5-37e9b86ecfc8.png)

In the above example, Jarvis will say "Hello World" out loud.

From a terminal, you can use `curl`:
```
$> curl "http://192.168.1.20:8080?say=Hello%20World"
[{"answer":"Hello World"}]
```
To have `curl` encoding the url for you, use two arguments:
* `-G` to send data with GET method
* `--data-urlencode` to encode special characters such as spaces in parameters
```
$> curl -G "http://192.168.1.20:8080" --data-urlencode "say=Hello World"
[{"answer":"Hello World"}]
```

You can make Jarvis listening directly for a command by simulating a hotword recognition:
```
$> curl "http://192.168.1.20:8080?action=listen"
[{"Success":"Ok"}]
```

You can also send orders to Jarvis:
```
$> curl -G "http://192.168.1.20:8080" --data-urlencode "order=bonjour Jarvis"
[{"answer":"Bonjour Alex"}]
```
To prevent the remote Jarvis from speaking, use the mute option:
```
$> curl -G "http://192.168.1.20:8080" --data-urlencode "order=météo" --data-urlencode "mute=true"
[{"answer":"je regarde..."},{"answer":"Ciel plutôt dégagé. Minimales : 4 degrés."}]
```
You can easily extract the answer from the `JSON`, ex using `jq`:
```
$> curl "http://192.168.1.20:8080?order=meteo&mute=true" | jq -r '.[1].Jarvis'
Ciel plutôt dégagé. Minimales : 3 degrés.
```
If you have defined an API Key for security, you have to pass it like this:
```
$> curl -G "http://192.168.1.20:8080" --data-urlencode "say=I am secured" --data-urlencode "key=12345"
[{"answer":"I am secured"}]
```
To retrieve the user commands:
```
$> curl "http://192.168.1.20:8080?action=get_commands"
*MERCI*==say "De rien"
*AIDE*==jv_display_commands
*COMMENT*APPELLE*==say "Je m'appelle $trigger"
[...]
```
To replace by a new set of commands (replace all):
```
$> curl -s -d '{"action":"set_commands","commands":"*MERCI*==say \"De rien\"\n*AIDE*==..."}'
{"status":"ok"}
```
To retrieve the user events:
```
$> curl "http://192.168.1.20:8080?action=get_events"
2       9       *       *       6,0     ~/jarvis/jarvis.sh -x "meteo"
0       7-20    *       *       1-5     ~/jarvis/jarvis.sh -x "quelle heure est-il"
[...]
```
To replace by a new set of events (replace all):
```
$> curl -s -d '{"action":"set_commands","commands":"2  9  *  *  6,0..."}'
{"status":"ok"}
```
To retrieve the user settings:
```
$> curl "http://192.168.1.20:8080?action=get_config"
{"username": "Alex", "version": "16.11.20", [...] }
```
To change settings (replace all):
```
$> curl -s -d '{"action":"set_config","config":"{\"username\":\"Alexylem\", [...]}"}' http://192.168.1.20:8080
{"status":"ok"}
```

## Author
[Alex](https://github.com/alexylem)
