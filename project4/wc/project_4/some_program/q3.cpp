#include <iostream>
#include <string>
using namespace std;

int main ()
{
    // string a ="132";
    // a += 116;
    // // cout << a;
    // // char v6 = -62 - *(_BYTE *)a[0];
    // // cout << v6;
    // char v6  = -67;
    // cout << (unsigned int)v6;
    string a;
    string b;
    for(int j = 0; j <=127; j++){

        a += j;
        char c;
        for(int i = 0; ;++i){
            if (i >= a.length()){
                break;
            }

            if(a[i] <= 67){
                c = -126 - a[i];
            }
            else{
                c = -62 - a[i];
            }
            // cout << c << " " << (unsigned int)c << endl;
            b += (unsigned int) c;
        }
        cout << b << " " << a << endl;
        a="";
        b="";
    }
}