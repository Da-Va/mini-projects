#include <stdio.h>
#include <stdbool.h>

#define loop while(true)

#define SUCCESS 0
#define ERROR_INPUT 100
    
#define INPUT_MAX 10000
#define INPUT_MIN -10000


int main()
{
    int count = 0;
    int even_count = 0;
    int odd_count = 0;
    int positive_count = 0;
    int negative_count = 0;
    int sum = 0;
    int min = INPUT_MAX;
    int max = INPUT_MIN;

    loop {
        int number;
        int scan_r = scanf("%d", &number);
        if (scan_r == EOF) break;
        if (scan_r != 1) {
            fprintf(stderr, "Error: Neplatny vstup!\n");
            return ERROR_INPUT;
        }
        if (number < INPUT_MIN || INPUT_MAX < number) {
            fprintf(stderr, "Error: Vstup je mimo interval!\n");
            return ERROR_INPUT;
        }
         
        count += 1;
        if (number % 2 == 0) {
            even_count += 1;
        } else {
            odd_count += 1;
        }
        if(number > 0) {
            positive_count += 1;
        } else if (number < 0) {
            negative_count += 1;
        }
        sum += number;
        
        min = number < min ? number : min;
        max = number > max ? number : max;
    }
    
    printf("Pocet cisel: %d\n", count);
    printf("Pocet kladnych: %d\n", positive_count);
    printf("Pocet zapornych: %d\n", negative_count);
    printf("Procento kladnych: %f\n", 100. * positive_count/count);
    printf("Procento zapornych: %f\n", 100. * negative_count/count);
    printf("Pocet sudych: %d\n", even_count);
    printf("Pocet lichych: %d\n", odd_count);
    printf("Procento sudych: %.2f\n", 100. * even_count/count);
    printf("Procento lichych: %.2f\n", 100. * odd_count/count);
    printf("Prumer: %.2f\n", (float)sum/count);
    printf("Maximum: %d\n", max);
    printf("Minimum: %d\n", min);

    return SUCCESS;
}