#/usr/bin/bash
printf "patching Multimedia\n"

NODE=$(pw-cli list-objects | grep -B 4 -A 1 '"route_multimedia"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')

printf "Multimedia found on ID $NODE\n"
printf "  setting volume to $1\n"

pw-cli s $NODE Props '{ monitorMute: false, monitorVolumes: [ '$1', '$1', '$1', '$1', '$1', '$1', '$1', '$1' ] }'

