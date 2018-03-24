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

class scannerTypes(fixedLabels):

    def __init__ (self) :
        pass

    def codegen(self):

        class_template = '''            

class ${TableName} {

public:

    ${TableName}();
   ~${TableName}();

    ${publicMember}
    ${publicMethod}

private:
    ${privateMember}
    ${privateMethod}
};

''' 


        sql_update_template = '''            
    std::string stmt = "UPDATE ${TableName} SET ";
    std::stringstream stmt_out;
    int firstEntry = 1;
    stmt_out << stmt ;
    ${Param};
    stmt_out << ";";

    return stmt_out.str(); 
''' 

        sql_select_template = '''            
    std::string stmt = "SELECT ";
    std::stringstream stmt_out;
    int firstEntry = 1;
    stmt_out << stmt ;
    ${Param}
    stmt_out << " FROM ${TableName} ;";
    return stmt_out.str();  
''' 




        print ".Scanning 'database.xlsx'"
        wb =  open_workbook('./database.xlsx')

        range_error_start = 301
        for sheet in wb.sheets():
            print "..Scanning (Table) "+sheet.name 

            self.db_types_h              = open('./'+sheet.name+'.h', 'w')  
            self.db_types_c              = open('./'+sheet.name+'.cpp', 'w')     
            self.db_types_h.write(self.header_cpp)
            self.db_types_c.write(self.header_cpp)
            self.db_types_c.write('\n#include <string>\n#include <sstream>\n#include \"'+sheet.name+'.h\"')

            num_rows  = sheet.nrows
            num_cells = sheet.ncols
            curr_row = 1 # 

            _publicMember = ""
            _publicMethod = "\n\tvoid CLEAR_VALID_BIT() { valid = 0; }"
            _publicMethod = _publicMethod + "\n\tvoid SET_ALL_VALID_BIT() { valid = 0xFFFFFFFF; }\n"
            _publicMethod = _publicMethod + "\n\tstd::string UPDATE_STMT();"
            _publicMethod = _publicMethod + "\n\tvoid UPDATE_STMT_PRE();"
            _publicMethod = _publicMethod + "\n\tstd::string SELECT_STMT();"
            _publicMethod = _publicMethod + "\n\tvoid SELECT_STMT_PRE();\n"
            _privateMember = "\n\tunsigned int valid;"
            _privateMethod = ""

            _sql_update_param = ""
            _sql_select_param = ""
 
            _ctor_init_list = ""
            while curr_row < num_rows:
                param_name    = sheet.cell_value(curr_row, 0).encode("utf-8").replace('.','_')
                param_type    = sheet.cell_value(curr_row, 1).encode("utf-8")
                param_min     = int(sheet.cell_value(curr_row, 2))
                param_max     = sheet.cell_value(curr_row, 3)
                if param_type.upper() == 'TEXT' :
                   param_default = sheet.cell_value(curr_row, 4).encode("utf-8")
                else:
                   param_default = int(sheet.cell_value(curr_row, 4))
                param_scope   = sheet.cell_value(curr_row, 5).encode("utf-8")
                
                print '>>>>', param_name

                # ctor/dtor
                if param_type.upper() == 'TEXT' :
                    if curr_row == 1 :
                        _ctor_init_list =   param_name+'("'+param_default+'")'
                    else:
                        _ctor_init_list =  _ctor_init_list + ','+ param_name+'("'+param_default+'")'
                else:
                    if curr_row == 1 :
                        _ctor_init_list =   param_name+'('+str(param_default)+')'
                    else:
                        _ctor_init_list =  _ctor_init_list + ','+ param_name+'('+str(param_default)+')'
                
                #define MIN
                self.db_types_h.write('\n\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_MIN '+str(param_min))
                #defien MAX
                if  param_type.upper() == 'ENUM' :
                    param_enum_list = param_max.encode("utf-8").split('|')
                    for idx, param_enum in enumerate(param_enum_list) :
                        self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_ENUM_'+param_enum.upper()+' '+str(int(idx+param_min)) )             
                    self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_MAX '+str(int(param_min+len(param_enum_list)-1)))
                else:
                    self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_MAX '+str(int(param_max)))
                #define DEFAULT
                if param_type.upper() == 'TEXT' :
                    self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_DEFAULT  "'+ param_default+'"' )
                else: 
                    self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_DEFAULT '+str(param_default))
                #define valid bit
                self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_VALID_FLAG   (0x1 << '+str(int( curr_row -1 ))+')')
                # define range_error
                self.db_types_h.write('\n#define '+sheet.name.upper()+'_'+param_name.upper()+'_RANGE_ERROR '+str(range_error_start))
                range_error_start = range_error_start + 1

                # class member : public or private
                if param_scope.upper() == 'PRIVATE' :
                    if param_type.upper() == 'TEXT' :
                        _publicMember   = _publicMember + '\n\tvoid set_'+param_name+'(std::string new_'+param_name+') { '+param_name+' = new_'+param_name+'; }'
                        _privateMember  = _privateMember + '\n\tstd::string '+param_name+'; /* internal parameter. filled by system call() */'
                    elif param_type.upper() == 'NUMBER' or param_type.upper() == 'INT' :
                        _publicMember   = _publicMember + '\n\tvoid set_'+param_name+'(int new_'+param_name+') { '+param_name+' = new_'+param_name+'; }'
                        _privateMember  = _privateMember + '\n\tint '+param_name+';  /* internal parameter. filled by system call() */'
                    else:
                        _privateMember  = _privateMember + '\n\tUNKNOWN '+param_name+'; // compilation error'
                else :
                    if param_type.upper() == 'TEXT' :
                        _publicMember   = _publicMember +  '\n\tstd::string '+param_name+';'
                    else :
                        _publicMember  = _publicMember + '\n\tint '+param_name+';'
               
                # method declaration SET_VALID_BIT
                _publicMethod = _publicMethod + '\n\tvoid SET_VALID_BIT_'+param_name.upper()+'();'
                _publicMethod = _publicMethod + '\n\tvoid SET_CHANGE_BIT_'+param_name.upper()+'();'

                # method impl SET_VALID_BIT
                self.db_types_c.write('\n\nvoid '+sheet.name+'::SET_VALID_BIT_'+param_name.upper()+'() { valid = valid | (0x1 << '+str(curr_row-1)+'); }')
                self.db_types_c.write('\n\nvoid '+sheet.name+'::SET_CHANGE_BIT_'+param_name.upper()+'() { if ( '+ param_name +' != '+sheet.name.upper()+'_'+param_name.upper()+'_DEFAULT )  valid = valid | (0x1 << '+str(curr_row-1)+'); }')
                
                
                ####################################
                # sql_stmt
                if  param_scope.upper() != 'PRIVATE'  :
                    if param_type.upper() == 'TEXT' :
                         _sql_update_param = _sql_update_param + '\n\tif ( '+sheet.name.upper()+'_'+param_name.upper()+'_VALID_FLAG & valid ) {\n\t\tif (firstEntry) { firstEntry = 0; stmt_out << "'+param_name.upper()+'=\\"" << '+param_name+' << "\\""; }\n\t\telse {  stmt_out << ",'+param_name.upper()+'=\\"" << '+param_name+' << "\\"";}\n\t}'
                    else:
                         _sql_update_param = _sql_update_param + '\n\tif ( '+sheet.name.upper()+'_'+param_name.upper()+'_VALID_FLAG & valid ) {\n\t\tif (firstEntry) { firstEntry = 0; stmt_out << "'+param_name.upper()+'=" << '+param_name+'; }\n\t\telse {  stmt_out << ",'+param_name.upper()+'=" << '+param_name+';}\n\t}'
        
                    _sql_select_param = _sql_select_param + '\n\tif ( '+sheet.name.upper()+'_'+param_name.upper()+'_VALID_FLAG & valid ) {\n\t\tif (firstEntry) { firstEntry = 0; stmt_out << " '+param_name.upper()+'"; } else { stmt_out << " , '+param_name.upper()+'"; } \n\t}\n'
                #
              
                # ^^^^^^ repeat ^^^^^^^^
                curr_row = curr_row + 1
            
            # range check 
            _publicMethod = _publicMethod + '\n\tint rangeCheck( ) { /* not implemented */ return 300; }'

            stmts = Template(class_template).safe_substitute(dict(TableName=sheet.name, \
                     publicMember = _publicMember, publicMethod = _publicMethod, privateMember = _privateMember, privateMethod = _privateMethod )) 
            
            self.db_types_h.write(stmts)
            ###################################################
            # sql_stmt
    
            stmt = Template(sql_select_template).safe_substitute(dict(TableName=sheet.name.upper(), \
                     Param = _sql_select_param ))
            self.db_types_c.write('\n\nstd::string '+sheet.name+'::SELECT_STMT() { \n'+stmt+'\n}\n')
            stmt = Template(sql_update_template).safe_substitute(dict(TableName=sheet.name.upper(), \
                     Param = _sql_update_param ))
            self.db_types_c.write('\n\nstd::string '+sheet.name+'::UPDATE_STMT() { \n'+stmt+'\n}\n')
            

            ####################################################
            # ctor/dtor
            self.db_types_c.write('\n'+sheet.name+'::~'+sheet.name+'() {}')
            self.db_types_c.write('\n'+sheet.name+'::'+sheet.name+'():'+_ctor_init_list+' {}')
            self.db_types_h.close()          
            self.db_types_c.close() 

