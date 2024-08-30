#!/usr/bin/sh
printf "Linking Virtual Nodes...\n"

printf "Linking: ALC1220-VB-DT Front Out [USB] =[ FL FR ]=> Comms Microphone\n"
pw-link ALC1220-VB-DT_rear_mic_usb:capture_FL route_comms_mic:input_FL --passive
pw-link ALC1220-VB-DT_rear_mic_usb:capture_FR route_comms_mic:input_FR --passive

printf "Linking: Multimedia =[ FL FR ]=> Comms Speakers\n"
pw-link route_multimedia:capture_FL route_comms_speakers:playback_FL --passive
pw-link route_multimedia:capture_FR route_comms_speakers:playback_FR --passive

printf "Linking: Multimedia =[ FL FR ]=> ALC1220-VB-DT Front Out [USB]\n"
pw-link route_multimedia:capture_FL ALC1220-VB-DT_front_out_usb:playback_FL --passive
pw-link route_multimedia:capture_FR ALC1220-VB-DT_front_out_usb:playback_FR --passive

printf "Linking: Comms Speakers =[ FL FR RL RR FC LFE SL SR ]=> ALC1220-VB-DT Front Out [USB]\n"
pw-link route_comms_speakers:capture_FL ALC1220-VB-DT_rear_out_usb:playback_FL --passive
pw-link route_comms_speakers:capture_FR ALC1220-VB-DT_rear_out_usb:playback_FR --passive
pw-link route_comms_speakers:capture_RL ALC1220-VB-DT_rear_out_usb:playback_RL --passive
pw-link route_comms_speakers:capture_RR ALC1220-VB-DT_rear_out_usb:playback_RR --passive
pw-link route_comms_speakers:capture_FC ALC1220-VB-DT_rear_out_usb:playback_FC --passive
pw-link route_comms_speakers:capture_LFE ALC1220-VB-DT_rear_out_usb:playback_LFE --passive
pw-link route_comms_speakers:capture_SL ALC1220-VB-DT_rear_out_usb:playback_SL --passive
pw-link route_comms_speakers:capture_SR ALC1220-VB-DT_rear_out_usb:playback_SR --passive

printf "Linked Virtual Nodes\n"

printf "Patching: Comms Microphone\n"
NODE_COMMS_MIC=$(pw-cli list-objects | grep -B 4 -A 1 '"route_comms_mic"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')
pw-cli s $NODE_COMMS_MIC Props '{ params: [channelmix.disable: true], volume: 2 }'

printf "Patched Comms Microphone\n"
