import json

class DatabaseFormatter:
    #Simple class that takes a database scheme in json format and does three things
    #1) Format a json into a sql insert table command
    #2) Check if a input dicts contains all the required fieds in the correct type
    #2b) format a dict into a sql insert command
    TYPES_DICT = {int: "integer", float: "real", str: "text"}

    def  __init__(self, tables_scheme):
        super().__init__()
        assert type(tables_scheme) is dict
        self.tables_scheme = tables_scheme

    @classmethod
    def from_file(cls, tables_scheme_filename):
        tables_scheme = dict(json.loads(tables_scheme_filename))
        return cls(tables_scheme = tables_scheme)
        
    def _get_field_sql_insert_table(self, table):
        out_command = "("
        for field in table.keys():
            out_command += " " + field
            out_command += " " + self.TYPES_DICT[type(field)] + ","

        return out_command + ")"

                
    def get_insert_tables(self, table_scheme):
        '''
        Returns a dict that contains the name of the table and
        the corresponding sql command to insert the fields
        ex : {songs: "(path text, embed int)"}
        '''

        tables_dict = []
        for table in table_scheme.keys():
            tables_dict[table] = "INSERT INTO" + table \
            + self._get_field_sql_insert_table(table) 
            idx += 1

    def get_insert_value(self, val, table_name):
        '''
        Transform a result dict into an sql command
        CARE: this will only work if the values in the res dict
        are in the same order as the fields in the table !!!
        '''
        #TODO: Fix this :)
        out_command = "INSERT INTO " + table_name \
            + " VALUES (" 

        #Should first check if the dict is valid and correspond to the scheme
        for item in val.keys():
            out_command += item

        return out_command

