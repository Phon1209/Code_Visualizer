#include <stdio.h>

int arr[] = {1, 2, 3, 4, 5};
int arr2d[][3] = {{1,2,3}, {4,5,6}, {7,8,9}, {10,11,12}};
void doubled(int *p_arr)
{
  for (int i = 0; i < 5; i++)
  {
    p_arr[i] *= 2;
  }
}

typedef int MyVar;

int main()
{
  char x = 'G';
  MyVar c = 6;
  const int a = 3;
  doubled(arr);
  int b = 7;
}
