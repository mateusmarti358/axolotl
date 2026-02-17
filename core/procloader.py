import importlib
import sys
import yaml

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

class ProcLoader:
    def __init__(self, config_path: str='defaults.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
    def load(self, proc_path: str):
        module_path = None
        class_name = None

        try:
            module_path = parse_proc_module(proc_path)
            module = importlib.import_module(module_path)

            class_name = parse_procname_class(proc_path)
            processor_class = getattr(module, class_name)

            params = self.config.get(class_name)

            return (processor_class, params)
        except (ImportError, AttributeError) as e:
            print(f"Erro: Processador '{module_path}' não encontrado.")
            print(f"Verifique se '{proc_path.lower()}' existe e contém a classe '{class_name}'.")
            sys.exit(1)
