from reader.abstract_file_reader import AbstractFileReader
import numpy as np
import pyexcel as pyx


class CsvReader(AbstractFileReader):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.wb = pyx.get_book(file_name=filename)
        
    def get_sheets(self):
        for name in self.wb.to_dict():
            sheet = self.wb[name].to_array()
            sheet = np.array(sheet)
            yield sheet
    
    def get_sheet_by_index(self, idx):
        sheet = self.wb.sheet_by_index(idx).to_array()
        sheet = np.array(sheet)
        return sheet
