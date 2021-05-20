
import pandas as pd
import re


class get_TM_names_list():
    def __init__(self, modules=[]):
        self.modules = modules

    def get_TM_names(modules):
        TMs_list = []
        mod_list = []
        for module in modules:
            TM_name = ''
            if 'TM' in module:
                mod_list = module.split('\n')
            for item in mod_list:
                if item == '':
                    mod_list.remove(item)
                    TM_name = mod_list[0]
            TMs_list.append(TM_name)
        # print(TMs_list)
        return TMs_list[1:]

    def get_PZ_list(PZs):
        # Read in excel file from Drive

        location = []
        for index, row in PZs.iterrows():
            location.append(row['PZ-Name1'])
        return location


def main():
    modules = ''
    with open('Porsche_TM_vereinfacht.txt') as f:
        # Read the file fully and as string. Name it TM
        TM = f.read()
        # Split TM by "----------" to seperate each module
        modules = TM.split("----------")
    get_TMs = get_TM_names_list.get_TM_names(modules)
    # get_TMs.get_TM_names(modules)
    get_TMs

if __name__ == "__main__":
    main()
