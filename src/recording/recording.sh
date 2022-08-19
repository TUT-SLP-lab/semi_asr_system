#!/bin/bash

device="$(pactl get-default-sink).monitor"
#device="DummyOutput0.monitor"
exec parec --file-format=wav --device=$device > "./record-data/tmp.wav"
