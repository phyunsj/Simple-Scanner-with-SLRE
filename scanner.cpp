#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <cstdlib>
#include "slre.h"


using namespace std;

typedef struct _addr
{
   char name[50];
   char street[100];
   char city[50];
   char state[20];
   int  postal;
} ADDR;

const int MAX_CAPTURES = 10;

int scanner( char *filename,  ADDR &addr) {
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

      if (!slre_match(&regEngine, line.c_str(), strlen(line.c_str()), caps)) {
        cout << "[ERR] not valid format line : " << line << endl;

      } else {

        cout << "full match  : " <<  caps[0].len << "." << caps[1].ptr << endl;
        cout << "key         : " <<  caps[1].len << "." << caps[1].ptr << endl;
        cout << "value       : " <<  caps[2].len << "." << caps[2].ptr << endl;
        

        if ( caps[2].len > 0 ) {
           string key(caps[1].ptr, caps[1].len);
           string value(caps[2].ptr, caps[2].len);
           if ( !strncmp ( caps[1].ptr, "name", caps[1].len) ) {
              strncpy( addr.name, caps[2].ptr, 50);
           }
           if ( !strncmp ( caps[1].ptr, "street", caps[1].len) ) {
              strncpy( addr.street, caps[2].ptr, 100);
           }
           if ( !strncmp ( caps[1].ptr, "city", caps[1].len) ) {
              strncpy( addr.city, caps[2].ptr, 50);
           }
           if ( !strncmp ( caps[1].ptr, "state", caps[1].len) ) {
              strncpy( addr.state, caps[2].ptr, 20);
           }
           if ( !strncmp ( caps[1].ptr, "zip", caps[1].len) ) {
              addr.postal = atoi(caps[2].ptr);
           }
        }
      }
    }

  infile.close();
  return 0;    
}

int main(int agc, char *argv[]) {

   ADDR address;
   memset( &address, 0, sizeof(ADDR));

   if( scanner( argv[1] , address ) != 0 ) cout << "scanner error" << endl;;
   
   cout << endl << "RESULT ====================" << endl;
   cout << "NAME   : "<< address.name << endl;
   cout << "STREET : "<< address.street << endl;
   cout << "CITY   : "<< address.city << endl;
   cout << "STATE  : "<< address.state << endl;
   cout << "ZIP    : "<< address.postal << endl;
   return 0;
}