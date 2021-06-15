#include <iostream>
#include <string>

using namespace std;

int main(){
    string a2 = "";
    unsigned long long v6;
    unsigned long long v3;

    for ( int i = 32; ; ++i )
    {
        string a1 = "";
        v3 = i;
        if ( v3 >= 128 )
        {
            break;
        }
        if ( i <= 67 )
        {
            v6 = -126 - i;
        }
        else
        {
            v6 = -62 - i;
        }

        a1 += (unsigned long long)v6;
        if(a1 == "f"){
            cout << "f: " << (char)i << endl;
        }else if(a1 == "l"){
            cout << "l: " << (char)i << endl;
        }else if(a1 == "a"){
            cout << "a: " << (char)i << endl;
        }else if(a1 == "g"){
            cout << "g: " << (char)i << endl;
        }
    }
    return 0;
}