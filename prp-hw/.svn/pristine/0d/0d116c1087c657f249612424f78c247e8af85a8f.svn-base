#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <ctype.h>

#define loop while(1)

#define PRIME_LIMIT 1000000

#define SUCCESS 0
#define ERROR_INPUT 100
#define ERROR_DECOMPOSITION 110

#define HIGH_WORD_64(B) (B >> 32)
#define LOW_WORD_64(B) ((B << 32) >> 32)


#define LARGE_INT_MAX_DEC_DIGITS 100
#define LARGE_INT_CELL_COUNT 11  // Should be enough

typedef struct {
    uint32_t cells[LARGE_INT_CELL_COUNT];   // Little-endian ordering
} large_int_t;


uint32_t add_to_cell(uint32_t *cell, uint32_t a)
{
    uint64_t buffer = (uint64_t)*cell + a;

    *cell = LOW_WORD_64(buffer); 
    return HIGH_WORD_64(buffer);
}

uint32_t mult_cell(uint32_t *cell, uint32_t a)
{
    uint64_t buffer = (uint64_t)*cell * a;

    *cell = LOW_WORD_64(buffer); 
    return HIGH_WORD_64(buffer);
}

void large_int_add(large_int_t *number, uint32_t a)
{
    uint32_t overflow = add_to_cell(&number->cells[0], a);
    for(int i = 1; i < LARGE_INT_CELL_COUNT && overflow > 0; ++i) {
        overflow = add_to_cell(&number->cells[i], overflow);
    }
    assert(overflow == 0);
}

void large_int_mult(large_int_t *number, uint32_t a)
{
    uint32_t overflow = mult_cell(&number->cells[0], a);        
    for(int i = 1; i < LARGE_INT_CELL_COUNT; ++i) {
        uint32_t tmp = mult_cell(&number->cells[i], a);
        overflow = tmp + add_to_cell(&number->cells[i], overflow);
    }     
    assert(overflow == 0);
}

uint32_t large_int_mod(large_int_t *number, uint32_t a)
{
    uint32_t mod = 0;
    for(int i = LARGE_INT_CELL_COUNT - 1; i >= 0; --i) {
        mod = (((uint64_t)mod << 32) + number->cells[i]) % a;        
    }
    return mod;
}

void large_int_divide(large_int_t *number, uint32_t a)
{
    uint32_t mod = 0;
    for(int i = LARGE_INT_CELL_COUNT - 1; i >= 0; --i) {
        uint64_t buffer = ((uint64_t)mod << 32) + number->cells[i];
        mod = buffer % a;        
        number->cells[i] = buffer / a;
    }
}

bool large_int_equals(const large_int_t *large_numer, uint32_t a)
{
    if(large_numer->cells[0] != a) return false;
    for(int i = 1; i < LARGE_INT_CELL_COUNT; ++i) {
        if(large_numer->cells[i] != 0) {
            return false;
        }
    }
    return true;
}

bool large_int_load(large_int_t *out)
{
    for(int i = 0; i < LARGE_INT_CELL_COUNT; ++i) {
        out->cells[i] = 0;
    }
    
    int first_char;
    do {
        first_char = getchar();
    } while (isspace(first_char));
    if(!isdigit(first_char)) {
        return false;
    }
    large_int_add(out, first_char - '0');
    loop {
        int c = getchar();
        if(!isdigit(c)) {
            break; 
        }
        large_int_mult(out, 10);
        large_int_add(out, c - '0');
    }
    
    return true;
}

void large_int_print(large_int_t number)
{
    int n_digits = 0;
    char digits[LARGE_INT_MAX_DEC_DIGITS];

    while(!large_int_equals(&number, 0)) {
        digits[n_digits++] = '0' + large_int_mod(&number, 10);        
        large_int_divide(&number, 10);
    }
    for(int i = n_digits - 1; i >= 0; --i) {
        putchar(digits[i]);
    }
}


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

bool print_decomposition(large_int_t number, uint32_t primes[], uint32_t n_primes)
{
    printf("Prvociselny rozklad cisla "); 
    large_int_print(number);
    printf(" je:\n");

    if(large_int_equals(&number, 1)) {
        printf("1\n");
        return true;
    }
    
    for(int i = 0; i < n_primes && !large_int_equals(&number, 1); ++i) {
        uint32_t prime = primes[i];
        int power = 0;
        while (large_int_mod(&number, prime) == 0) {
            power += 1;            
            large_int_divide(&number, prime);
        }

        if(power > 0)  {
            printf("%d", prime);            
            if(power > 1) {
                printf("^%d", power);
            }
            if(!large_int_equals(&number, 1)) {
                printf(" x ");
            }
        }
    } 
    putchar('\n');
    return large_int_equals(&number, 1);
}

int main()
{
    uint32_t primes[PRIME_LIMIT];
    uint32_t n_primes = find_primes(primes, PRIME_LIMIT);
    
    loop {
        large_int_t number;
        if(!large_int_load(&number)) {
            fprintf(stderr, "Error: Chybny vstup!\n");
            return ERROR_INPUT;
        }
        if(large_int_equals(&number, 0)) break;
        
        if(!print_decomposition(number, primes, n_primes)) {
            fprintf(stderr,
                "Error: Decomposition contains a prime larger than %d\n",
                PRIME_LIMIT);
            return ERROR_DECOMPOSITION;
        }
    } 

    return SUCCESS;    
}