#include <iostream> //input output library
using namespace std; //using standareds 

int main()
{
    string food =  "pizza";
    string* ptr = &food;

    cout<<food<<endl;
    cout<<ptr<<endl;
    cout<<&food<<endl;
}