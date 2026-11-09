#/usr/bin/bash
printf "patching Comms Microphone\n"

NODE_COMMS_MIC=$(pw-cli list-objects | grep -B 4 -A 1 '"route_comms_mic"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')

printf "Comms Microphone found on ID $NODE_COMMS_MIC\n"
printf "  setting volume to $1\n"

#pw-cli s $NODE Props '{ monitorMute: false, monitorVolumes: [ '$1', '$1' ] }'
#pw-cli s $NODE Props '{ mute: false, channelVolumes: [ '$1', '$1' ] }'
#pw-cli s $NODE Props '{ channelmix.upmix: true, resample.disable: false, volume: '$1' }'
pw-cli s $NODE_COMMS_MIC Props '{ params: [{ channelmix.disable: true }], volume: '$1' }'

