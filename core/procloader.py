import importlib
import sys
import os

def parse_proc_module(procname: str):
    return '.'.join('.'.join(procname.split('/')).split('.')[:-1])

def parse_procname_class(procpath: str):
    procpath = procpath.split('/')[-1].capitalize().split('.')[0]
    chars = list(procpath)
    i = 0
    while i < len(chars):
        if chars[i] == '_':
            chars.pop(i)
            if i < len(chars):
                chars[i] = chars[i].upper()
        i += 1
    return "".join(chars)

def load_processor_class(processor_path: str):
    module_path = None
    class_name = None
    try:
        module_path = parse_proc_module(processor_path)
        module = importlib.import_module(module_path)

        class_name = parse_procname_class(processor_path)
        processor_class = getattr(module, class_name)

        return processor_class
    except (ImportError, AttributeError) as e:
        print(f"Erro: Processador '{module_path}' não encontrado.")
        print(f"Verifique se '{processor_path.lower()}' existe e contém a classe '{class_name}'.")
        sys.exit(1)
