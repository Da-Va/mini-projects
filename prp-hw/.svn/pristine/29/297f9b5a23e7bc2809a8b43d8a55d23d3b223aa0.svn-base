#include <stdio.h>
#include <stdbool.h>

#define SUCCESS 0
#define ERROR_INPUT 100
#define ERROR_ZERO_DIVISION 101

#define INPUT_MAX 10000
#define INPUT_MIN -10000

bool is_in_range(int n)
{
    return INPUT_MIN < n && n < INPUT_MAX;
}

void print_results(int a, int b)
{
    printf("Desitkova soustava: %d %d\n", a, b);
    printf("Sestnactkova soustava: %x %x\n", a, b);
    
    printf("Soucet: %d + %d = %d\n", a, b, a + b);
    printf("Rozdil: %d - %d = %d\n", a, b, a - b);

    printf("Soucin: %d * %d = %d\n", a, b, a * b);
    if (b != 0) {
        printf("Podil: %d / %d = %d\n", a, b, a / b);
    } else {
        printf("Podil: %d / %d = NaN\n", a, b);
    }

    printf("Prumer: %f\n", 0.5 * (a + b));
}

int main()
{
    int a;
    int b;     
    if(scanf("%d %d", &a, &b) != 2) {
        fprintf(stderr, "Chyba nacitani vstupu!\n");
        return ERROR_INPUT;
    }
    if(!is_in_range(a) || !is_in_range(b)) {
        fprintf(stderr, "Error: Vstup je mimo interval\n");
        return ERROR_INPUT;
    }
    
    print_results(a, b);

    if (b == 0) {
        fprintf(stderr, "Error: Nedefinovany vysledek!\n");
        return ERROR_ZERO_DIVISION;
    } 
    
    return SUCCESS;
}