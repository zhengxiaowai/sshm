#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from utils import check_python

@click.group()
def cli():
    pass

@cli.command()
def sync():
    click.echo('sync')

@cli.command()
def add():
    click.echo('add')

@cli.command()
def delete():
    click.echo('del')

@cli.command()
def update():
    click.echo('update')

@cli.command()
def list():
    click.echo('list')


if __name__ == '__main__':
    check_python()
    cli()
