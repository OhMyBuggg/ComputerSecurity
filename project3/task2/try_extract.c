#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    char command[60] = "bash connection.sh";
    FILE *fptr = fopen("address_port.txt", "r");
    char *line = NULL;
    size_t len;
    getline(&line, &len, fptr);
    printf("%s %ld",line, strlen(line));
}