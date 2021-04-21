import easygui
import os

def _save_file_dialogs(extension = "png"):
        # If user cancels it defaults to the FIRST choice. We want default to be NO so I reverse the default of choices here. 
        #saveornot = easygui.buttonbox(msg="Quer salvar a imagem?", choices = ("Não", "Sim") )
        #if saveornot == "Sim":
        #else:
        #    return None
        filename = easygui.filesavebox(msg = "Onde você quer salvar a imagem? (extensão %s será adicionada automaticamente)?" %(extension))
        if filename is None:
            return None
        filename = filename + "." + extension
        if os.path.exists(filename):
            ok_to_overwrite = easygui.buttonbox(msg="Imagem %s já existe. Sobrescrever?" %(filename), choices = ("Não", "Sim") )
            if ok_to_overwrite == "Sim":
                return filename
            else:
                return None
        else:
            return filename