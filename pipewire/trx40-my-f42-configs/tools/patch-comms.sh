#/usr/bin/bash
printf "patching Comms Speakers\n"

NODE=$(pw-cli list-objects | grep -B 4 -A 1 '"route_comms_speakers"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')

printf "Comms Speakers found on ID $NODE\n"
printf "  setting volume to $1\n"

pw-cli s $NODE Props '{ monitorMute: false, monitorVolumes: [ '$1', '$1', '$1', '$1', '$1', '$1', '$1', '$1' ] }'

