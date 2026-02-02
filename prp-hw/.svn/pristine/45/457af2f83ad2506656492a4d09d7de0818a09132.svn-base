#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>

#define loop while(1)
#define MIN(X, Y) ((X < Y) ? X : Y)

#define SUCCESS 0
#define ERROR_INPUT 100
#define ERROR_INPUT_LENGTH 101
#define ERROR_MEMORY 110

#define DYNAMIC_STRING_INIT_CAPACITY 10

char *dynamic_string_load()
{
    char *str = malloc(DYNAMIC_STRING_INIT_CAPACITY * sizeof(char));
    if(str == NULL) {
        return NULL;
    }
    int capacity = DYNAMIC_STRING_INIT_CAPACITY;
    int length = 0;
    
    loop {
        int c = getchar();        
        if(c == '\n') break;
        
        if(length >= capacity - 1) {
            char *tmp = realloc(str, capacity + capacity/2);
            if(tmp == NULL) {
                free(str);
                return NULL;
            }
            str = tmp; 
            capacity += capacity/2;
        }
        str[length++] = c;
    }
    str[length] = '\0';

    return str;
}

int str_length(const char *str)
{
    int length = 0; 
    for(; str[length] != '\0'; ++length);
    return length;
}

bool str_equal(const char *str1, const char *str2)
{
    int i;
    for(i = 0; str1[i] != '\0' && str2[i] != '\0'; ++i) {
        if (str1[i] != str2[i]) {
            return false;
        }
    }
    return str1[i] == str2[i];
}

bool input_is_valid(const char *str)
{
    for(int i = 0; str[i] != '\0'; ++i) {
        char c = str[i];
        if(!('a' <= c && c <= 'z') && !('A' <= c && c <= 'Z')) {
            return false; 
        }
    }
    return true;
}

int hamming_distance(const char *str1, const char *str2)
{
    int hamming = 0;
    for(int i = 0; str1[i] != '\0'; ++i) {
        if(str1[i] != str2[i]) {
            hamming += 1;
        }
    }
    return hamming;
}

int levensthein_distance(const char *str1, const char *str2)
{
    int len1 = str_length(str1);
    int len2 = str_length(str2);

    int dist[len1 + 1][len2 + 1];
    for(int i = 0; i < len1 + 1; ++i) {
        dist[i][0] = i;
    }
    for(int i = 0; i < len2 + 1; ++i) {
        dist[0][i] = i;
    }

    for(int i = 0; i < len1; ++i) {
        for(int j = 0; j < len2; ++j) {
            dist[i + 1][j + 1] = dist[i][j] + ((str1[i] == str2[j]) ? 0 : 1);
            dist[i + 1][j + 1] = MIN(dist[i][j + 1] + 1, dist[i + 1][j + 1]);
            dist[i + 1][j + 1] = MIN(dist[i + 1][j] + 1, dist[i + 1][j + 1]);
        }
    }

    return dist[len1][len2];
}

char shift_char(char c, int offset)
{
    char block_end = ((c >> 5) & 1) ? 'z' : 'Z';
    char other_block_begin = ((c >> 5) & 1) ? 'A' : 'a';
    
    if(c + offset <= block_end) {
        return c + offset;
    } else {
        return c + offset - block_end + other_block_begin - 1;
    }
}

void shift_string(const char *src, char *dst, int offset)
{
    int i;
    for(i = 0; src[i] != '\0'; ++i) {
        dst[i] = shift_char(src[i], offset);
    }
    dst[i] = '\0';
}

int find_offset(
    const char* encrypted,
    const char* corrupted,
    int(*dist_f)(const char*, const char*)
) {
    char str_buff[str_length(encrypted) + 1];
    int min_dist = INT_MAX;
    int min_offset = 0;
    for(int offset = 0; offset <= 'z'-'a' + 'Z'-'A'; ++offset) {
        shift_string(encrypted, str_buff, offset);
        int dist = dist_f(str_buff, corrupted);
        if(dist < min_dist) {
            min_dist = dist;
            min_offset = offset;
        }
    }
    return min_offset;
}

void print_shifted(const char* str, int offset)
{
    for(int i = 0; str[i] != '\0'; ++i) {
        putchar(shift_char(str[i], offset));
    }
}

int main(int argc, char *argv[])
{
    int status = SUCCESS;
    
    char *encrypted_msg = dynamic_string_load(&encrypted_msg);
    char *corrupted_msg = dynamic_string_load(&corrupted_msg);

    if(encrypted_msg == NULL || corrupted_msg == NULL) {
        fprintf(stderr, "Error: Chyba alokace!\n");
        status = ERROR_MEMORY;
        goto main_return; 
    }
    
    if(!input_is_valid(encrypted_msg) || !input_is_valid(corrupted_msg)) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        status = ERROR_INPUT; 
        goto main_return;
    }
    
    int offset;
    if(argc > 1 && str_equal(argv[1], "-prp-optional")) {
        offset = find_offset(encrypted_msg, corrupted_msg, levensthein_distance);
    } else {
        if(str_length(encrypted_msg) != str_length(corrupted_msg)) {
            fprintf(stderr, "Error: Chybna delka vstupu!\n");
            status = ERROR_INPUT_LENGTH;
            goto main_return;
        }
        
        offset = find_offset(encrypted_msg, corrupted_msg, hamming_distance);
    }
    
    print_shifted(encrypted_msg, offset);
    putchar('\n');

    main_return:
    free(encrypted_msg);
    free(corrupted_msg);
    return status;
}