#!/usr/bin/micropython

from os import system
import socket
from time import sleep
from json import dumps

def read_values(filename: str) -> list:
    file = open(filename)
    lines = file.readlines()
    n = len(lines)
    val1 = int(lines[0])
    val2 = int(lines[1])
    file.close()
    return [val1, val2]


def get_gpio_values() -> list | None:
    gpio1 = " 1"
    gpio2 = " 2"
    script = "./get_gpio_values.sh"
    ret = system(script + gpio1 + gpio2)
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
    addr = "192.168.1.2"
    port = 10000
    gpio_data = [0, 0]
    while True:
        new_data = get_gpio_values()
        if new_data == None:
            print("failed to obtain gpio values")
        else:
            if new_data != gpio_data:
                send_data(new_data, addr, port)
                gpio_data = new_data
                print("data sent")
        sleep(0.05)


main_loop()

