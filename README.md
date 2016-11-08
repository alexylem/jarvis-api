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
$> curl -d '{"say":"Hello World"}' http://192.168.1.20:8080
[{"Jarvis":"Hello World"}]
```
In the above example, Jarvis will say "Hello World" out loud.

You can also send orders to Jarvis:
```
$> curl -d '{"order":"bonjour"}' http://192.168.1.20:8080
[{"Jarvis":"Bonjour Alex"}]
```
To prevent the remote Jarvis from speaking, use the mute option:
```
$> curl -d '{"order":"meteo","mute":"true"}' http://192.168.1.20:8080
[{"Jarvis":"je regarde..."},{"Jarvis":"Ciel plutôt dégagé. Minimales : 4 degrés."}]
```
You can easily extract the answer from the `JSON`, ex using `jq`:
```
$> curl -s -d '{"order":"meteo","mute":"true"}' http://192.168.1.20:8080 | jq -r '.[1].Jarvis'
Ciel plutôt dégagé. Minimales : 3 degrés.
```

## Author
[Alex](https://github.com/alexylem)
