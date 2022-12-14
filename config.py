'''Class to deal with the config file'''

import configparser
import copy

class Config():
    def __init__(self,config_file):
        self.parser = configparser.ConfigParser(inline_comment_prefixes='#')
        #config.optionxform=str
        self.parser.optionxform = str
        self.parser.read(config_file)
        self.sections = self.parser.sections() 

    def sec(self,section):
        return dict(self.parser.items(section))

    def __repr__(self):
        '''Output when printing an instance of this class'''
        for sect in self.parser.sections():
          print('Section:', self.sect)
          for k,v in parser.items(sect):
             print(' {} = {}'.format(k,v))
          print()

    def __call__(self,section=None,par = None,dtype = None):
        '''Output when returning an instance of this class'''
        if section == None:
            return copy.deepcopy(self.parser.sections) 
        elif par is None:
            return dict(self.parser.items(section)) 
        elif dtype == 'int':
            return self.parser.getint(section,par)
        elif dtype == 'float':
            return self.parser.getfloat(section,par)
        elif dtype == 'bool':
            return self.parser.getboolean(section,par)
        elif dtype == 'str':
            return self.parser.get(section,par) 
    
    def update_config(self,section, par,val):
        self.parser.set(section,par,val)
  
