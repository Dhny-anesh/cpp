#include <iostream>  // import input output library
using namespace std; 

class adding  // creating class
{
    public:  //access specifier 
    int a,b; // initialize variables 
    int sum;
    
    void function()
    {
        cout<<"enter 1st variable"<<endl;
        cin>>a;
        cout<<"enter 2nd variable"<<endl;
        cin>>b;
    }

};


int main()
{
    adding add;  
    add.function();
    add.sum = add.a+add.b;
    cout<<"addition is ="<<add.sum;


}