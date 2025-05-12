#!/bin/bash

sinks=$(pactl list sinks | grep "Name: " | sed -e s%"Name: "%%g | tr '\n' ',' | sed 's/.$//')
IFS="," read -ra parts <<< "$sinks"
default_sink=$(pactl get-default-sink)
for part in "${parts[@]}"; do
	sink=$(echo "$part" | xargs)
	if [[ "$sink" != "$default_sink" ]]; then
   		echo "Changing audio sink from $default_sink to $sink..."
		pactl set-default-sink $sink
	fi
done
