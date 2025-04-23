#!/usr/bin/sh

###############################################################################
# CONFIG
###############################################################################

COMMS_SRC=route_comms_mic
COMMS_SINK=route_comms_speakers
COMMS_MONO_TO_STEREO_SRC=remap_output.comms.mono-to-stereo
COMMS_MONO_TO_STEREO_SINK=remap_input.comms.mono-to-stereo
COMMS_SURROUND_TO_STEREO_SRC=effect_output.comms.surround-to-stereo
COMMS_SURROUND_TO_STEREO_SINK=effect_input.comms.surround-to-stereo

MULTI_SINK=route_multimedia
MULTI_SURROUND_TO_STEREO_SRC=effect_output.multimedia.surround-to-stereo
MULTI_SURROUND_TO_STEREO_SINK=effect_input.multimedia.surround-to-stereo

SOUND_CARD_SRC=alsa_input.usb-Focusrite_Scarlett_4i4_4th_Gen_S4E1EVT3B05E67-00.Direct__hw_Gen__source
SOUND_CARD_SINK=alsa_output.usb-Focusrite_Scarlett_4i4_4th_Gen_S4E1EVT3B05E67-00.Direct__hw_Gen__sink

###############################################################################
# LINK NODES
###############################################################################

printf "Linking: Scarlett =[ FL ]=> Mono -> Stereo [Comms]\n"
pw-link ${SOUND_CARD_SRC}:capture_FR ${COMMS_MONO_TO_STEREO_SINK}:playback_FL --passive

printf "Linking: Stereo [Comms] =[ FL FR ]=> Comms Microphone\n"
pw-link ${COMMS_MONO_TO_STEREO_SRC}:capture_FL ${COMMS_SRC}:input_FL --passive
pw-link ${COMMS_MONO_TO_STEREO_SRC}:capture_FR ${COMMS_SRC}:input_FR --passive

printf "Linking Virtual Nodes...\n"

# printf "Linking: ALC1220-VB-DT Front Out [USB] =[ FL FR ]=> Comms Microphone\n"
# pw-link ALC1220-VB-DT_rear_mic_usb:capture_FL route_comms_mic:input_FL --passive
# pw-link ALC1220-VB-DT_rear_mic_usb:capture_FR route_comms_mic:input_FR --passive

printf "Linking: Multimedia =[ FL FR RL RR FC LFE SL SR ]=> Comms Speakers\n"
pw-link ${MULTI_SINK}:capture_FL ${COMMS_SINK}:playback_FL --passive
pw-link ${MULTI_SINK}:capture_FR ${COMMS_SINK}:playback_FR --passive
pw-link ${MULTI_SINK}:capture_RL ${COMMS_SINK}:playback_RL --passive
pw-link ${MULTI_SINK}:capture_RR ${COMMS_SINK}:playback_RR --passive
pw-link ${MULTI_SINK}:capture_FC ${COMMS_SINK}:playback_FC --passive
pw-link ${MULTI_SINK}:capture_LFE ${COMMS_SINK}:playback_LFE --passive
pw-link ${MULTI_SINK}:capture_SL ${COMMS_SINK}:playback_SL --passive
pw-link ${MULTI_SINK}:capture_SR ${COMMS_SINK}:playback_SR --passive

printf "Linking: Comms Speakers =[ FL FR RL RR FC LFE SL SR ]=> Surround -> Stereo [Comms]\n"
pw-link ${COMMS_SINK}:capture_FL ${COMMS_SURROUND_TO_STEREO_SINK}:playback_FL --passive
pw-link ${COMMS_SINK}:capture_FR ${COMMS_SURROUND_TO_STEREO_SINK}:playback_FR --passive
pw-link ${COMMS_SINK}:capture_RL ${COMMS_SURROUND_TO_STEREO_SINK}:playback_RL --passive
pw-link ${COMMS_SINK}:capture_RR ${COMMS_SURROUND_TO_STEREO_SINK}:playback_RR --passive
pw-link ${COMMS_SINK}:capture_FC ${COMMS_SURROUND_TO_STEREO_SINK}:playback_FC --passive
pw-link ${COMMS_SINK}:capture_LFE ${COMMS_SURROUND_TO_STEREO_SINK}:playback_LFE --passive
pw-link ${COMMS_SINK}:capture_SL ${COMMS_SURROUND_TO_STEREO_SINK}:playback_SL --passive
pw-link ${COMMS_SINK}:capture_SR ${COMMS_SURROUND_TO_STEREO_SINK}:playback_SR --passive

printf "Linking: Multimedia =[ FL FR RL RR FC LFE SL SR ]=> Surround -> Stereo [Multimedia]\n"
pw-link ${MULTI_SINK}:capture_FL ${MULTI_SURROUND_TO_STEREO_SINK}:playback_FL --passive
pw-link ${MULTI_SINK}:capture_FR ${MULTI_SURROUND_TO_STEREO_SINK}:playback_FR --passive
pw-link ${MULTI_SINK}:capture_RL ${MULTI_SURROUND_TO_STEREO_SINK}:playback_RL --passive
pw-link ${MULTI_SINK}:capture_RR ${MULTI_SURROUND_TO_STEREO_SINK}:playback_RR --passive
pw-link ${MULTI_SINK}:capture_FC ${MULTI_SURROUND_TO_STEREO_SINK}:playback_FC --passive
pw-link ${MULTI_SINK}:capture_LFE ${MULTI_SURROUND_TO_STEREO_SINK}:playback_LFE --passive
pw-link ${MULTI_SINK}:capture_SL ${MULTI_SURROUND_TO_STEREO_SINK}:playback_SL --passive
pw-link ${MULTI_SINK}:capture_SR ${MULTI_SURROUND_TO_STEREO_SINK}:playback_SR --passive

printf "Linking: Surround -> Stereo [Comms] =[ FL FR ]=> Scarlett [ FL FR ]\n"
pw-link ${COMMS_SURROUND_TO_STEREO_SRC}:capture_FL ${SOUND_CARD_SINK}:playback_FC --passive
pw-link ${COMMS_SURROUND_TO_STEREO_SRC}:capture_FR ${SOUND_CARD_SINK}:playback_LFE --passive
printf "Linking: Surround -> Stereo [Multimedia] =[ FL FR ]=> Scarlett [ RL RR ]\n"
pw-link ${MULTI_SURROUND_TO_STEREO_SRC}:capture_FL ${SOUND_CARD_SINK}:playback_FL --passive
pw-link ${MULTI_SURROUND_TO_STEREO_SRC}:capture_FR ${SOUND_CARD_SINK}:playback_FR --passive

# printf "Linking: Multimedia =[ FL FR ]=> ALC1220-VB-DT Front Out [USB]\n"
# pw-link ${MULTI_SINK}:capture_FL ALC1220-VB-DT_front_out_usb:playback_FL --passive
# pw-link ${MULTI_SINK}:capture_FR ALC1220-VB-DT_front_out_usb:playback_FR --passive

# printf "Linking: Comms Speakers =[ FL FR RL RR FC LFE SL SR ]=> ALC1220-VB-DT Front Out [USB]\n"
# pw-link ${COMMS_SINK}:capture_FL ALC1220-VB-DT_rear_out_usb:playback_FL --passive
# pw-link ${COMMS_SINK}:capture_FR ALC1220-VB-DT_rear_out_usb:playback_FR --passive
# pw-link ${COMMS_SINK}:capture_RL ALC1220-VB-DT_rear_out_usb:playback_RL --passive
# pw-link ${COMMS_SINK}:capture_RR ALC1220-VB-DT_rear_out_usb:playback_RR --passive
# pw-link ${COMMS_SINK}:capture_FC ALC1220-VB-DT_rear_out_usb:playback_FC --passive
# pw-link ${COMMS_SINK}:capture_LFE ALC1220-VB-DT_rear_out_usb:playback_LFE --passive
# pw-link ${COMMS_SINK}:capture_SL ALC1220-VB-DT_rear_out_usb:playback_SL --passive
# pw-link ${COMMS_SINK}:capture_SR ALC1220-VB-DT_rear_out_usb:playback_SR --passive

printf "Linked Virtual Nodes\n"

###############################################################################
# PATCH NODES
###############################################################################

printf "Patching: Comms Microphone\n"
NODE_COMMS_MIC=$(pw-cli list-objects | grep -B 4 -A 1 '"route_comms_mic"' | grep type | sed 's/,.*// ' | awk '{ print substr( $0, 5 ) }')
pw-cli s $NODE_COMMS_MIC Props '{ params: [channelmix.disable: true], volume: 2 }'

printf "Patched Comms Microphone\n"
