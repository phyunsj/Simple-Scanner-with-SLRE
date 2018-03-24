#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <cstdlib>
#include "slre.h"
#include "sqlite3.h"


using namespace std;

#include "db_class_types.include" // <- Mapreduce class declared here
static sqlite3 *db = NULL;
const int MAX_CAPTURES = 10;
#define debug_ 1


int scanner( char *filename) {
    // RegEx
    struct slre        regEngine;
    struct cap         caps[MAX_CAPTURES];
    string line;
    ifstream infile(filename);

    if ( !infile.is_open() ) return -1;
    
    if ( !slre_compile(&regEngine, "^(\\S+)=(\\S+)")) {
      cout << "[ERR] compiling RE: " << regEngine.err_str << endl;
      infile.close();
      return -1;
    }
    
    while (getline(infile, line)) {

#include "db_read_from_map.include"

    }

    infile.close();
    return 0;    
}

int main(int argc, char *argv[]) {

  int rc; // SQL return code
  char *zErrMsg = 0;


  // Check the number of parameters
  if (argc < 3) {
        // help 
        std::cerr << "Usage: " << argv[0] << " direction filename" << std::endl;
        std::cerr << "        direction: 0(.map => table), 1 (table => .map) " << std::endl;
        
        return 1;
  }


  // open db
  sqlite3_open("./hadoop.db",&db);
  if (!db) std::cout << "\t[SQL] the database didn't open." << std::endl;
  else std::cout << "[SQL] hadoop.db open." << std::endl;

  if (atoi(argv[1]) == 1 ) {
    // Read MAPREEUCE table and save only non-default memebrs.
    mapreduce_instance.SET_ALL_VALID_BIT(); // read all but public members only
    std::string execStmt =  mapreduce_instance.SELECT_STMT();  
    std::cout << "SQL : " << execStmt << std::endl;
    sqlite3_stmt* stmt;
    if(sqlite3_prepare_v2(db, execStmt.c_str() , -1, &stmt, NULL) != SQLITE_OK) {
      std::cout << "SQL compilation error: " << sqlite3_errmsg(db) << std::endl;
      sqlite3_finalize(stmt);
      return -1;
    }

    // MAPREDUCE table has a single entry. 
    while((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
#include "db_read_from_record.include"
    }
    if(rc != SQLITE_DONE) {
        //this error handling could be done better, but it works
        std::cout << "SQL ERROR: while performing sql: " << sqlite3_errmsg(db) << std::endl;
        std::cout << "ret_code = " << rc << std::endl;
        return -1;
    }

    // only write different from DEFAULT
    ofstream outfile(argv[2]);

#include "db_write_to_map.include"

    outfile << stmt_out.str();
    outfile.close();
    
    sqlite3_finalize(stmt);

  } else {

    // Read .map file and assign to Mapreduce class members
    if( scanner( argv[2] ) != 0 ) cout << "scanner error" << endl;
    
    // UPDATE SQL stmt generation. All valid bits are set so that all settigns become defualt. 
    std::string execStmt =  mapreduce_instance.UPDATE_STMT(); 
    std::cout << "SQL : " << execStmt << std::endl;
    rc = sqlite3_exec(db, execStmt.c_str(), NULL, NULL, &zErrMsg);
    if( rc != SQLITE_OK ) {
         std::cout << "SQL error: "<< zErrMsg << std::endl;
         sqlite3_free(zErrMsg);
         exit(-1);
    } 

  }

  // close db
  if (db)  sqlite3_close(db);
  return 0;
}