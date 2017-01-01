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
$> ./jarvis.sh
Starting RestAPI server on http://192.168.1.20:8080
Jarvis: Bonjour Alex
...
```
Now you can control Jarvis from another device.

Make Jarvis say something:
```
$> curl "http://192.168.1.20:8080?say=Hello World"
[{"Jarvis":"Hello World"}]
```
In the above example, Jarvis will say "Hello World" out loud.

You can also send orders to Jarvis:
```
$> curl "http://192.168.1.20:8080?order=bonjour"
[{"Jarvis":"Bonjour Alex"}]
```
To prevent the remote Jarvis from speaking, use the mute option:
```
$> curl "http://192.168.1.20:8080?order=meteo&mute=true"
[{"Jarvis":"je regarde..."},{"Jarvis":"Ciel plutôt dégagé. Minimales : 4 degrés."}]
```
You can easily extract the answer from the `JSON`, ex using `jq`:
```
$> curl "http://192.168.1.20:8080?order=meteo&mute=true" | jq -r '.[1].Jarvis'
Ciel plutôt dégagé. Minimales : 3 degrés.
```
If you have defined an API Key for security, you have to pass it like this:
```
$> curl "http://192.168.1.20:8080?say=I am secured&key=12345
[{"Jarvis":"I am secured"}]
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
