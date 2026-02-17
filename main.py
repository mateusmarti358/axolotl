import click

from core.app import App
from core.procloader import load_processor_class

def get_procs(procs):
    processors = []
    for p in procs:
        proclass = load_processor_class(p)
        params: dict = proclass.get_default_params()
        processors.append((proclass, params))
    return processors

def print_params(params):
    for k, v in params.items():
        print(f'\t{k} = {v}')

def print_procs(procs):
    for i, p in enumerate(procs):
        print(f'{i + 1}: {p[0].__name__}')
        if p[1] is None:
            continue

        print_params(p[1])

def config_proc(proc):
    print(f'{proc[0].__name__} params:')
    print_params(proc[1])

    while True:
        i = input(f'key: ')
        
        if proc[1].get(i) is None:
            print('Invalid param name.')
            continue

        print(f'{i} = {proc[1][i]}')
        val = input('value [\\c: cancel]: ')
        if val == '\\c':
            break

        proc[1][i] = val
        break

def config_params(procs):
    ask = True
    while ask:
        i = input(f'Change any? [0 or empty = proceed] [1-{len(procs)}]: ')
        if len(i) == 0 or i == '0':
            ask = False
            continue

        idx = int(i)
        if idx < 1 or idx > len(procs):
            print("Invalid index.")
            continue

        proc = procs[idx - 1]
        if proc[1] is None:
            print('No params.')
            continue

        config_proc(proc)

@click.command()
@click.argument('img_path')
@click.argument('procs', nargs=-1)
@click.option('--feedback', is_flag=True)
def main(img_path, procs, feedback):
    processors = get_procs(procs)
    print_procs(processors)
    config_params(processors)

    app = App(img_path, processors)
    app.run()

if __name__ == "__main__":
    main()
