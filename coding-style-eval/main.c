#include <stdio.h>
#include <stdlib.h>

/* The main program */
int main(int argc, char *argv[])
{
  int first = 1;
  int number, count = 0, positive = 0, negative = 0, even = 0, odd = 0;
  int max = -10000, min = 10000;
  double sum = 0;

  while (scanf("%d", &number)== 1){
    if (number<-10000 || number>10000){
      printf("\nError: Vstup je mimo interval!\n");
      return 100;
    }
    if (!first){
      printf(", ");
    }
    else{
      first = 0;
    }
    printf("%d", number);

    count++;
    sum += number;
    if (number < 0) negative++;
    if (number > 0) positive++;
    if (number % 2 == 0) even++;
    else odd++;
    if (number > max) max = number;
    if (number < min) min = number;
  }

   if (count > 0) {
        printf("\n");
        printf("Pocet cisel: %d\n", count);
        printf("Pocet kladnych: %d\n", positive);
        printf("Pocet zapornych: %d\n", negative);
        printf("Procento kladnych: %.2f\n", (double)positive / count * 100);
        printf("Procento zapornych: %.2f\n", (double)negative / count * 100);
        printf("Pocet sudych: %d\n", even);
        printf("Pocet lichych: %d\n", odd);
        printf("Procento sudych: %.2f\n", (double)even / count * 100);
        printf("Procento lichych: %.2f\n", (double)odd / count * 100);
        printf("Prumer: %.2f\n", sum / count);
        printf("Maximum: %d\n", max);
        printf("Minimum: %d\n", min);
    }


  return 0;
}

