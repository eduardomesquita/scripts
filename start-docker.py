#!/usr/bin/python2.5

import subprocess
import argparse
import os

def imprime(*out):
    if(args.log):
        print ''.join([str(p) for p in out if p])

def executar(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    imprime(out, err)
    return out

def get_container():
    container = executar('docker inspect --format="{{.Id}}" focused_morse')
    return container

def add_network():
    executar('ip link set dev docker0 down')
    executar('ip addr del 172.17.42.1/16 dev docker0')
    executar('ip addr del 172.17.42.1/16 dev docker0')
    executar('ip addr del 192.168.99.100/16 dev docker0')
    executar('ip addr add 192.168.99.100/24 dev docker0')
    executar('ip link set dev docker0 up')
    executar('ip link set dev br0 down')
    executar('ip addr show docker0')

def start():
    add_network()
    executar('systemctl start docker.socket')
    executar('systemctl start docker.service')
    

def stop():
    executar('systemctl stop docker.socket')
    executar('systemctl stop docker.service')


def init():
    container = get_container()

    if 'Cannot connect' in container:
        imprime('iniciando docker...')
        start()
    else:
        imprime('parando docker...')
        executar('docker stop ' + container)
        stop()
        start()

    executar('docker start ' + container )


def is_root():
    user = os.getenv("SUDO_USER")
    if user is None:
        args.log=True
        imprime('This program need \'sudo\'')
        exit()




if __name__ == '__main__':

     parser = argparse.ArgumentParser()
     parser.add_argument('-log', '--log', help='Ativar logger', action='store_true')
     args = parser.parse_args()

     is_root()
     init()
