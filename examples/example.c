#include <stdio.h>

int main()
{
  int arr[20] = {1};
  int x = 20;
  int a[3] = {1, 3, 5};
  char *c = "Hello World!";
  // char c = 'g';
  int *p = &x;
  for (int i=0;i<3;i++)
  {
    a[i] *=2;
    *p *= 2;
  }

  *p -= 20;
}

