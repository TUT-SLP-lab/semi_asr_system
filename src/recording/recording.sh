#!/bin/bash

#device="$(pactl get-default-sink).monitor"
device="alsa_output.pci-0000_65_00.1.hdmi-stereo-extra1.monitor"
exec parec --file-format=wav --format=s16le --channels=2 --device=$device > "./record-data/tmp.wav"