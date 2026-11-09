#1/usr/bin/bash
echo patching skype

NODE=$(pw-cli list-objects | grep -B 5 -A 1 '"Skype"' | grep -B 6 '"Stream/Output/Audio"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')

printf "Skype found on ID $NODE\n"
printf "  setting volume to $1\n"

pw-cli s $NODE Props '{ mute: false, channelVolumes: [ '$1', '$1' ] }'
