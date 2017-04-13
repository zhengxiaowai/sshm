#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import readline
import click
import json
from six.moves import input as raw_input
from dropbox.files import WriteMode
from collections import defaultdict
from clients import get_client, init_client, get_supported_platform
from utils import prompt_line, mkdir, convert_binary_type


@click.group()
def cli():
    pass


@cli.command()
@click.option('--platform', required=True, type=click.Choice(get_supported_platform()))
def init(platform):
    init_client(platform)


@cli.command()
def add():
    client = get_client()
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

        ssh_config['identityfile'] = prompt_line(
            'IdentityFile[{}]: ',
            ssh_config['identityfile'],
            (ssh_config['identityfile'],))

        ok = raw_input(json.dumps(ssh_config, indent=4) +
                       '\nare you sure? [Y/N]: ')
        ok = ok.strip()

        if ok.lower() == 'y':
            break
        else:
            continue

    overwrite_mode = WriteMode('overwrite')
    hostname = ssh_config['hostname']
    identityfile = ssh_config['identityfile']

    if identityfile:
        with open(identityfile) as f:
            cert_content = convert_binary_type(f.read())
            cert_filename = '/{}.cert'.format(hostname)
            client.upload(cert_content, cert_filename, mode=overwrite_mode)

    config_filename = '/{}.json'.format(hostname)
    ssh_config = convert_binary_type(json.dumps(ssh_config, indent=4))
    client.upload(ssh_config, config_filename, mode=overwrite_mode)


@cli.command()
def list():
    client = get_client()
    for entry in client.list('').entries:
        filename = entry.name
        if filename.endswith('.json'):
            click.echo(os.path.splitext(filename)[0])


@cli.command()
@click.argument('hostname')
def info(hostname):
    client = get_client()
    path = '/{}.json'.format(hostname)
    content = client.download(path)
    click.echo(content)


@cli.command()
@click.argument('hostname')
def delete(hostname):
    client = get_client()
    ssh_json = '/{}.json'.format(hostname)
    ssh_cert = '/{}.cert'.format(hostname)
    client.delete(ssh_json)
    client.delete(ssh_cert)


@cli.command()
@click.argument('hostname')
def connect(hostname):
    client = get_client()
    ssh_json = '/{}.json'.format(hostname)
    content = client.download(ssh_json)
    ssh_config = json.loads(content)
    local_ssh_cert_path = ''

    if ssh_config.get('identityfile', None):
        ssh_cert_path = '/{}.cert'.format(hostname)
        ssh_cert_filename = '{}.cert'.format(hostname)
        home_env = os.getenv('HOME', None)
        local_ssh_cert_dir = os.path.join(home_env, '.sshr_certs')
        mkdir(local_ssh_cert_dir)
        local_ssh_cert_path = os.path.join(
            local_ssh_cert_dir, ssh_cert_filename)

        content = client.download(ssh_cert_path)
        with open(local_ssh_cert_path, 'w') as f:
            f.write(str(content))

        os.chmod(local_ssh_cert_path, 0o600)

    user = ssh_config['user']
    host = ssh_config['host']
    port = ssh_config['port']
    ssh_command = ''
    if local_ssh_cert_path:
        ssh_command = 'ssh {}@{} -p {} -i {}'.format(
            user, host, port, local_ssh_cert_path)
    else:
        ssh_command = 'ssh {}@{} -p {}'.format(
            user, host, port)

    # mac Sierra(10.12.2)   ssh-add -K
    os.system(ssh_command)

    if local_ssh_cert_path:
        os.remove(local_ssh_cert_path)


if __name__ == '__main__':
    cli()
