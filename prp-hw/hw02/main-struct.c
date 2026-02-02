#include <stdio.h>
#include <stdbool.h>

#define loop while(true)

#define SUCCESS 0
#define ERROR_INPUT 100
    
#define INPUT_MAX 10000
#define INPUT_MIN -10000

typedef struct {
    int count;
    int even_count;
    int odd_count;
    int positive_count;
    int negative_count;
    int sum;
    int min;
    int max;
} data_t;

void reset_data(data_t *data)
{
    data->count = 0;
    data->even_count = 0;
    data->odd_count = 0;
    data->positive_count = 0;
    data->negative_count = 0;
    data->sum = 0;
    data->min = INPUT_MAX;
    data->max = INPUT_MIN;
}

typedef enum {
    load_data_InvalidInput,
    load_data_OutOfRange,
    load_data_OK
} load_data_return_t;
load_data_return_t load_data(data_t *data)
{
    loop {
        int number;
        int scan_r = scanf("%d", &number);
        if (scan_r == EOF) break;
        if (scan_r != 1) {
            return load_data_InvalidInput;
        }
        if (number < INPUT_MIN || INPUT_MAX < number) {
            return load_data_OutOfRange;
        }
         
        data->count += 1;
        if (number % 2 == 0) {
            data->even_count += 1;
        } else {
            data->odd_count += 1;
        }
        if(number > 0) {
            data->positive_count += 1;
        } else if (number < 0) {
            data->negative_count += 1;
        }
        data->sum += number;
        
        data->min = number < data->min ? number : data->min;
        data->max = number > data->max ? number : data->max;
    }
    return load_data_OK; 
}

void print_stats(const data_t *data)
{
    printf("Pocet cisel: %d\n", data->count);
    printf("Pocet kladnych: %d\n", data->positive_count);
    printf("Pocet zapornych: %d\n", data->negative_count);
    printf("Procento kladnych: %f\n", 100. * data->positive_count/data->count);
    printf("Procento zapornych: %f\n", 100. * data->negative_count/data->count);
    printf("Pocet sudych: %d\n", data->even_count);
    printf("Pocet lichych: %d\n", data->odd_count);
    printf("Procento sudych: %.2f\n", 100. * data->even_count/data->count);
    printf("Procento lichych: %.2f\n", 100. * data->odd_count/data->count);
    printf("Prumer: %.2f\n", (float)data->sum/data->count);
    printf("Maximum: %d\n", data->max);
    printf("Minimum: %d\n", data->min);
}


int main()
{
    data_t data;
    reset_data(&data);

    load_data_return_t load_status = load_data(&data);
    if (load_status == load_data_InvalidInput) {
        fprintf(stderr, "Error: Neplatny vstup!\n");
        return ERROR_INPUT;
    }
    if (load_status == load_data_OutOfRange) {
        fprintf(stderr, "Error: Vstup je mimo interval!\n");
        return ERROR_INPUT;
    }
    
    print_stats(&data);

    return SUCCESS;
}