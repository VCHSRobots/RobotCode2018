#include <Python.h>

int dotprouducts(float arr1[], float arr2[]) {
    int times = sizeof(arr1)/4;
    float dots = 0;
    for(times; times >= 0; --times) {
        dots = dots + (arr1[times] * arr2[times]);
    }
    return(dots);
}


static PyObject* parselist()


int main() {
    float x[3] = {1, 2, 3};
    float y[3] = {1, 2, 3};
    int dots = dotprouducts(x, y);
    return 0;
}

void initmyModule()