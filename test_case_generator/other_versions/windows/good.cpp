#include <iostream>
#include <math.h>
#include <string>

using namespace std;

bool swap(int& a,int& b){
    int t = a;
    a = b;
    b = t;
    return true;
}

int min (int a , int b)
{
    if (a < b) return a;
    return b;  
}

int main()
{
    int z1 , z2 ,z3 ;
    std :: cin >> z1 >> z2 >> z3 ;
    if (z1 > z2) swap(z1,z2);
    if (z2 > z3) swap(z2,z3);
    if (z1 > z2) swap(z1,z2);
    string ans = "triangle";
    //string str1 = "Hello";
    if (z3 >= z1 + z2)
    {
        std :: cout << "can't be a triangle" << std :: endl ;
        ans = ""; 
        return 0;
    }
    
    if(z1 == z2 || z2 == z3 ) ans = "isosceles triangle";
    if(z1 == z2 && z2 == z3 ) ans = "equilateral triangle";
    if(z1 * z1 + z2 * z2 == z3 * z3) ans = "right angled triangle";
  
   std :: cout << ans << std :: endl; 
}
