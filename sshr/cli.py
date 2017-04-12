#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import readline
import click
import json
from dropbox.files import WriteMode
from collections import defaultdict
from client import DropboxClient

dbxc = DropboxClient()


@click.group()
def cli():
    pass


@cli.command()
def add():
    ssh_config = defaultdict(str)

    while True:
        ssh_config['hostname'] = prompt_line(
            'HostName[{}]: ',
            ssh_config['hostname'],
            (ssh_config['hostname'],))

        ssh_config['host'] = prompt_line(
            'Host[{}]: ',
            ssh_config['host'],
            (ssh_config['host'],))

        ssh_config['port'] = prompt_line(
            'Port[{}]: ',
            ssh_config['port'],
            (ssh_config['port'],))

        ssh_config['user'] = prompt_line(
            'User[{}]: ',
            ssh_config['user'],
            (ssh_config['user'],))

        ok = raw_input(json.dumps(ssh_config, indent=4) +
                       '\nare you sure? [Y/N]: ')
        ok = ok.strip()

        if ok.lower() == 'y' or ok == '':
            break
        else:
            continue

    config_filename = '/{}.json'.format(ssh_config['hostname'])
    ssh_config = json.dumps(ssh_config, indent=4)
    dbxc.upload(ssh_config, config_filename, mode=WriteMode('overwrite'))


@cli.command()
def list():
    for entry in dbxc.list('').entries:
        filename = entry.name
        if filename.endswith('.json'):
            click.echo(os.path.splitext(filename)[0])


@cli.command()
@click.argument('hostname')
def info(hostname):
    path = '/{}.json'.format(hostname)
    mata, res = dbxc.download(path)
    click.echo(res.content)


@cli.command()
@click.argument('hostname')
def connect(hostname):
    path = '/{}.json'.format(hostname)
    mata, res = dbxc.download(path)
    ssh_config = json.loads(res.content)

    user = ssh_config['user']
    host = ssh_config['host']
    port = ssh_config['port']
    os.system('ssh {}@{} -p {}'.format(user, host, port))


@cli.command()
@click.argument('hostname')
def delete(hostname):
    path = '/{}.json'.format(hostname)
    dbxc.delete(path) 

if __name__ == '__main__':
    cli()
