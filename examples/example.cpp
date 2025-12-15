#include <stdio.h>

int arr[] = {1, 2, 3, 4, 5};
void doubled(int *arr)
{
  for (int i = 0; i < 5; i++)
  {
    arr[i] *= 2;
  }
}

typedef int MyVar;

int main()
{
  MyVar c = 6;
  const int a = 3;
  doubled(arr);
  int b = 7;
}
