#include <stdio.h>
#include <stdint.h>

#define loop while(1)

#define PRIME_LIMIT 1000000
typedef uint32_t uint32_t;

#define SUCCESS 0
#define ERROR_INPUT 100
#define ERROR_DECOMPOSITION 110

uint32_t find_primes(uint32_t array[], uint32_t limit)
{
    uint32_t n_primes = 0;
    for(uint32_t i = 0; i < limit; ++i) {
        array[i] = 1;
    }     
    for(uint32_t i = 2; i < limit; ++i) {
        if (array[i]) {
            array[n_primes++] = i;
            for(uint32_t j = i+i; j < limit; j+=i) {
                array[j] = 0;                 
            }
        }
    }     
    return n_primes;
}

uint64_t print_decomposition(uint64_t number, uint32_t primes[], uint32_t n_primes)
{
    printf("Prvociselny rozklad cisla %lu je:\n", number);

    if(number == 1) {
        printf("1\n");
        return 1;
    }
    
    for(int pi = 0; pi < n_primes && number > 1; ++pi) {
        uint32_t prime = primes[pi];
        int power = 0;
        while (number % prime == 0) {
            power += 1;            
            number = number / prime;
        }

        if(power > 0)  {
            printf("%d", prime);            
            if(power > 1) {
                printf("^%d", power);
            }
            if(number > 1) {
                printf(" x ");
            }
        }
    } 
    putchar('\n');
    return number;
}

int main()
{
    uint32_t primes[PRIME_LIMIT];
    uint32_t n_primes = find_primes(primes, PRIME_LIMIT);
    
    loop {
        uint64_t number;
        if(scanf("%lu", &number) != 1 || number < 0) {
            fprintf(stderr, "Error: Chybny vstup!\n");
            return ERROR_INPUT;
        }
        if (number == 0) break;
        
        if(print_decomposition(number, primes, n_primes) > 1) {
            fprintf(stderr,
                "Error: Decomposition of %lu, contains a prime larger than %d\n",
                number, PRIME_LIMIT);
            return ERROR_DECOMPOSITION;
        }
    } 

    return SUCCESS;    
}