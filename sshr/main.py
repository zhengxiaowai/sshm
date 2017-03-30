#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from utils import check_python, check_cfg
from commands import add_command

@click.group()
def cli():
    pass


@cli.command()
def add():
    click.echo('add')
    add_command()

@cli.command()
def delete():
    click.echo('del')

@cli.command()
def update():
    click.echo('update')

@cli.command()
def list():
    click.echo('list')

@cli.command()
def sync():
    click.echo('sync')

if __name__ == '__main__':
    check_python()
    check_cfg()
    cli()
