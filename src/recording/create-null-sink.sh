#!/bin/bash

pactl list sinks short | grep DummyOutput0 > /dev/null || {
	pactl load-module module-null-sink sink_name=DummyOutput0 sink_properties=device.description=DummyOutput0
}
pactl set-default-sink DummyOutput0
