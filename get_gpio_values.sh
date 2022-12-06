#!/bin/sh

cat /sys/devices/platform/gpio-tr@0/gpiochip5/gpio/IO_$1/value > gpio_data
cat /sys/devices/platform/gpio-tr@0/gpiochip5/gpio/IO_$2/value >> gpio_data