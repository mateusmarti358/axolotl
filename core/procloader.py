import importlib
import sys
import os

def load_processor_class(processor_name: str):
    try:
        module_path = f"procs.{processor_name.lower()}"
        module = importlib.import_module(module_path)

        class_name = processor_name.capitalize() 
        processor_class = getattr(module, class_name)
        
        return processor_class
    except (ImportError, AttributeError) as e:
        print(f"Erro: Processador '{processor_name}' não encontrado.")
        print(f"Verifique se 'procs/{processor_name.lower()}.py' existe e contém a classe '{processor_name.capitalize()}'.")
        sys.exit(1)