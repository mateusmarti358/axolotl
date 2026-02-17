import click
from core.app import App
from core.procloader import load_processor_class

@click.command()
@click.argument('img_path')
@click.argument('procs', nargs=-1)
@click.option('--feedback', is_flag=True)
def main(img_path, procs, feedback):
    processadores = []
    for p in procs:
        processadores.append(load_processor_class(p))

    app = App('imgs/' + img_path, processadores)
    app.run()

if __name__ == "__main__":
    main()