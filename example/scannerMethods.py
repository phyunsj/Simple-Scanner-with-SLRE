#!/usr/bin/env python

from xlrd import open_workbook
from string import Template
import sys, pprint, os
import re
import time
import shutil

# Add the directory containing your module to the Python path (wants absolute paths)
scriptpath = "./fixedLabels.py"
sys.path.append(os.path.abspath(scriptpath))
from fixedLabels import *

class scannerMethods(fixedLabels):

    def __init__ (self) :   	
        # class definition 
        self.db_types_h          = open('./db_class_types.include', 'w')
        # 
        self.db_read_from_map    = open('./db_read_from_map.include', 'w')  
        # 
        self.db_write_to_map     = open('./db_write_to_map.include', 'w')   
        #
        self.db_read_from_record = open('./db_read_from_record.include', 'w') 

        # copyright oe customized comments
        self.db_types_h.write(self.header_cpp)
        self.db_read_from_map.write(self.header_cpp)
        self.db_write_to_map.write(self.header_cpp)
        self.db_read_from_record.write(self.header_cpp)

        # enum 
        self.db_counter = 400   # command enum starts from here
        self.db_types_h.write('\n/* COMMAND STARTS FROM : '+str(self.db_counter) +' */')
        self.db_types_h.write('\n\n#define COMMAND 300 '+str(self.db_counter))
        self.db_err_counter = 300
        self.db_types_h.write('\n/* ERROR CODE STARTS FROM :  '+str(self.db_counter) +' */')
        self.db_types_h.write('\n\n#define NO_ERROR  '+str(self.db_counter))

    def close(self):
        self.db_types_h.close()          
        self.db_read_from_map.close() 
        self.db_write_to_map.close() 
        self.db_read_from_record.close()


    def codegen(self):

        slre_read_from_map = '''

        if (!slre_match(&regEngine, line.c_str(), strlen(line.c_str()), caps)) {
           cout << "[ERR] not valid format line : " << line << endl;

        } else {

            cout << "full match  : " <<  caps[0].len << "." << caps[1].ptr << endl;
            cout << "key         : " <<  caps[1].len << "." << caps[1].ptr << endl;
            cout << "value       : " <<  caps[2].len << "." << caps[2].ptr << endl;
        

            if ( caps[2].len > 0 ) {
              string key(caps[1].ptr, caps[1].len);
              string value(caps[2].ptr, caps[2].len);
           
              ${strncmp}

            }
        }

'''
       

        print ".Scanning 'database.xlsx'"
        wb =  open_workbook('./database.xlsx')

        
        for sheet in wb.sheets():
            print '..Scanning (Table) '+sheet.name
            self.db_counter = self.db_counter + 1
            db_command = sheet.name.upper()
            num_rows  = sheet.nrows
            num_cells = sheet.ncols

            ########################################################################
            # .h for DB record
            #

            self.db_types_h.write('\n\n#define '+db_command.upper()+'_CREATE  '+str(self.db_counter))
            self.db_counter = self.db_counter + 1
            self.db_types_h.write('\n#define '+db_command.upper()+'_INSERT  '+str(self.db_counter))
            self.db_counter = self.db_counter + 1
            self.db_types_h.write('\n#define '+db_command.upper()+'_SELECT  '+str(self.db_counter))
            self.db_counter = self.db_counter + 1
            self.db_types_h.write('\n#define '+db_command.upper()+'_UPDATE  '+str(self.db_counter))
            self.db_counter = self.db_counter + 1
            self.db_types_h.write('\n#define '+db_command.upper()+'_DELETE  '+str(self.db_counter))
            self.db_counter = self.db_counter + 1
 
            self.db_types_h.write('\n\n#include "'+sheet.name+'.h"')
            self.db_types_h.write('\n'+sheet.name+'  '+sheet.name.lower()+'_instance;')

            curr_row = 1
            public_row = 0
            strncmp =''
            write_to_mapstmts ='\n\t\tstd::stringstream stmt_out;\n'
            read_from_dbstmts = ''
            while curr_row < num_rows:
                param_name    = sheet.cell_value(curr_row, 0).encode("utf-8")
                param_name_db = sheet.cell_value(curr_row, 0).encode("utf-8").replace('.','_')
                param_type    = sheet.cell_value(curr_row, 1).encode("utf-8")
                param_scope    = sheet.cell_value(curr_row, 5).encode("utf-8")
                
                print '>>>>', param_name
                if param_scope.upper() != 'PRIVATE' : 
                    #######################################################################
                    # read from map
                    #
                    if param_type.upper() == 'TEXT' :
                        strncmp = strncmp + '\n\t\t\tif ( !strncmp ( caps[1].ptr, "'+param_name+'", caps[1].len) ) { '+sheet.name.lower()+'_instance.SET_VALID_BIT_'+param_name_db.upper()+'();'+sheet.name.lower()+'_instance.'+param_name_db +' = std::string(caps[2].ptr); }'
                        read_from_dbstmts = read_from_dbstmts + '\n\t\t\t'+sheet.name.lower()+'_instance.'+param_name_db+' = (char *)sqlite3_column_text(stmt, '+ str(public_row)+');'
                        read_from_dbstmts = read_from_dbstmts + '\n\t\t\tif( debug_ ) std::cout << "'+param_name_db+' = " <<  '+sheet.name.lower()+'_instance.'+param_name_db+' << std::endl;'       
                    else:
                        strncmp = strncmp + '\n\t\t\tif ( !strncmp ( caps[1].ptr, "'+param_name+'", caps[1].len) ) { '+sheet.name.lower()+'_instance.SET_VALID_BIT_'+param_name_db.upper()+'();'+sheet.name.lower()+'_instance.'+param_name_db +' = atoi(caps[2].ptr); }'
                        read_from_dbstmts = read_from_dbstmts + '\n\t\t\t'+sheet.name.lower()+'_instance.'+param_name_db+' = sqlite3_column_int(stmt, '+ str(public_row)+');'
                        read_from_dbstmts = read_from_dbstmts + '\n\t\t\tif( debug_ ) std::cout << "'+param_name_db+' = " <<  '+sheet.name.lower()+'_instance.'+param_name_db+' << std::endl;'
                    #######################################################################
                    # write to map
                    #
                    write_to_mapstmts = write_to_mapstmts + '\n\t\tif ( '+sheet.name.lower()+'_instance.'+param_name_db+' != '+sheet.name.upper()+'_'+param_name_db.upper()+'_DEFAULT ) stmt_out << "'+param_name+'=" << '+sheet.name.lower()+'_instance.'+param_name_db +' << std::endl;'
                    public_row = public_row + 1
                curr_row = curr_row + 1
            read_from_mapstmts = Template(slre_read_from_map).safe_substitute(dict( strncmp = strncmp ))             
            self.db_read_from_map.write(read_from_mapstmts)

            self.db_write_to_map.write(write_to_mapstmts)
            self.db_read_from_record.write(read_from_dbstmts)
    