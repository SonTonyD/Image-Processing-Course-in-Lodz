import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', default="./Images/lenac.bmp", help='path of the image. Example:--name="./Images/lenac.bmp"  ')
def initdb(name):
    click.echo('Initialized the database')
    click.echo(name)

@cli.command()
def dropdb():
    click.echo('Dropped the database')
   
if __name__ == '__main__':
    cli()