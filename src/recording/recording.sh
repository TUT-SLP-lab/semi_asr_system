#!/bin/bash

device="$(pactl get-default-sink).monitor"
#device="DummyOutput0.monitor"
exec parec --file-format=wav --format=s16le --channels=1 --device=$device > "./record-data/tmp.wav"
