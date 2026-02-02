#include <stdio.h>
#include <stdbool.h>

#define LOG_ERR(MSG, ...) fprintf(stderr, MSG"\n", ##__VA_ARGS__)

#define SUCCESS 0
#define ERROR_INPUT 100
#define ERROR_INPUT_MSG "Error:Chybny vstup"
#define ERROR_OUT_OF_RANGE 101
#define ERROR_EVEN_WIDTH 102
#define ERROR_FENCE_SIZE 103

#define INPUT_MIN 3
#define INPUT_MAX 69

#define BASIC_DRAW_CHAR 'X'
#define BASIC_INFILL_CHAR ' '
#define FENCE_VERTICAL '|'
#define FENCE_HORIZONTAL '-'
#define ADVANCED_INFILL_ODD 'o'
#define ADVANCED_INFILL_EVEN '*'

void new_line()
{
    putchar('\n');
}

bool check_range(int n)
{
    return INPUT_MIN < n && n < INPUT_MAX; 
}

void print_roof_basic(int width)
{
    int mid = width/2 + 1;
    for(int row = 0; row < mid - 1; ++row) {
        int row_bound = mid + row;
        for(int col = 0; col < row_bound - 1; ++col) {
            if(col == mid - row - 1)  {
                putchar(BASIC_DRAW_CHAR);
            } else {
                putchar(' ');
            }
        }
        putchar(BASIC_DRAW_CHAR);
        new_line();
    }
}

void print_row_full(int width)
{
    for(int i = 0; i < width; ++i) {
        putchar(BASIC_DRAW_CHAR);
    }
}

void print_row_basic_infill(int width)
{
    putchar(BASIC_DRAW_CHAR);
    for(int i = 1; i < width - 1; ++i) {
        putchar(BASIC_INFILL_CHAR);
    }
    putchar(BASIC_DRAW_CHAR);
}

void print_walls_basic(int width, int height)
{
    print_row_full(width);
    new_line();
    for(int row = 1; row < height - 1; ++row) {
        print_row_basic_infill(width);
        new_line();
    }
    print_row_full(width);
    new_line();
}

void print_house_basic(int width, int height)
{
    print_roof_basic(width);    
    print_walls_basic(width, height);
}

void print_row_fence(int fence_size)
{
    for(int i = 0; i < fence_size; ++i) {
        if (i % 2 == fence_size % 2) {
            putchar(FENCE_HORIZONTAL);
        } else {
            putchar(FENCE_VERTICAL);
        }
    }
}

void print_row_advanced_infill(int width, int row)
{
    putchar(BASIC_DRAW_CHAR);
    for(int i = 1; i < width - 1; ++i) {
        if(i % 2 == row % 2) {
            putchar(ADVANCED_INFILL_ODD);
        } else {
            putchar(ADVANCED_INFILL_EVEN);
        }
    }
    putchar(BASIC_DRAW_CHAR);
}

void print_walls_advanced(int width, int height, int fence_size)
{
    print_row_full(width);
    new_line();
    for(int i = 1; i < height - 1; ++i) {
        print_row_advanced_infill(width, i);        
        if(i >= height - fence_size) {
            print_row_fence(fence_size);
        }
        new_line();
    }
    print_row_full(width);
    print_row_fence(fence_size);
    new_line();
    
}

void print_house_advanced(int width, int height, int fence_size)
{
    print_roof_basic(width);
    print_walls_advanced(width, height, fence_size);    
}

int main()
{
    int width;
    int height;
    
    if(scanf("%d %d", &width, &height) != 2) {
        LOG_ERR("Error: Chybny vstup!");
        return ERROR_INPUT;
    }
    if(!check_range(width) && !check_range(height)) {
        LOG_ERR("Error: Vstup je mimo interval!");
        return ERROR_OUT_OF_RANGE;
    }
    if(width % 2 == 0) {
        LOG_ERR("Error: Sirka neni liche cislo!");
        return ERROR_EVEN_WIDTH;
    }
    
    if(width == height) {
        int fence_size;
        if(scanf("%d", &fence_size) != 1) {
            LOG_ERR("Error: Chybny vstup!");
            return ERROR_INPUT;
        }
        if(fence_size >= height) { /* Unsure if should be >2 */
            LOG_ERR("Error: Neplatna velikost plotu!");
            return ERROR_FENCE_SIZE;
        }

        print_house_advanced(width, height, fence_size);
    } else {
        print_house_basic(width, height);     
    }
    
    return SUCCESS;
}