#!/usr/bin/micropython

from os import system
import socket
from sys import stderr
from time import sleep
from json import dumps, load

def read_values(filename: str) -> list:
    file = open(filename)
    lines = file.readlines()
    val1 = int(lines[0])
    val2 = int(lines[1])
    file.close()
    return [val1, val2]


def get_gpio_values(port1: int, port2: int) -> list | None:
    script = "./get_gpio_values.sh"
    ret = system(script + " " + str(port1) + " " + str(port2))
    if ret == 0:
        return read_values("gpio_data")
    else:
        return None


def send_data(values: list, addr: str, port: int):
    data = dumps({'value1': values[0], 'value2': values[1]})
    data = data.encode("utf-8")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    s.sendall(data)
    s.close()


def main_loop():
    conf_file = open('config.json')
    conf = load(conf_file)
    addr  = conf['server_addr']
    port = conf['server_port']
    update_period = conf['update_period_ms']
    gpio1 = conf['GPIO_1']
    gpio2 = conf['GPIO_2']

    gpio_data = [0, 0]
    while True:
        new_data = get_gpio_values(gpio1, gpio2)
        if new_data == None:
            print("failed to obtain gpio values", file=stderr)
        else:
            if new_data != gpio_data:
                send_data(new_data, addr, port)
                gpio_data = new_data
        sleep(update_period / 1000)

main_loop()

