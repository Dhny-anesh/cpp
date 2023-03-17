#include <iostream>
using namespace std;

class multiplication
{
    public:
    float a,b;
    float multiply;

    int inputoutput()
    {
        cout<< "enter the 1st value"<<endl;
        cin>>a;
        cout<<"enter the 2nd value"<<endl;
        cin>>b;
    }
};

int main()
{
    multiplication mul;
    mul.multiply = mul.a* mul.b;
    cout<<"multiplied value is "<<mul.multiply;
}

