#include <iostream>
#include "mul.hpp"

using namespace std;
int main()
{
    int a, b;
    int result;

    cout << "Enter two numbers: ";
    cin >> a >> b;

    result = mul(a, b);
    
    cout << "The product is: " << result << endl;
    return 0;
}