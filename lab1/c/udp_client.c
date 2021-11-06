#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SIZE 200000
#define N_MESSAGES 6

int create_socket_udp(){
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1){
        fprintf(stderr, "Error while creating socket\n");
        exit(1);
    }
    return sock;
}

void append_one_char(char* s, char c){
    int len = strlen(s);
    s[len] = c;
    s[len+1] = '\0';
}

void append_multiple_chars(char* s, char c, int amount){
    int i;
    for(i=0; i<amount; ++i){
        append_one_char(s, c);
    }
}

int pov(int a, int b){
    if (b == 0){
        return 1;
    }
    int res = 1;
    int i;
    for(i=0; i<b; ++i){
        res *= a;
    }
    return res;
}

struct sockaddr_in prepare_addr(int argc, char *argv[]){
    if (argc != 3){
        fprintf(stderr, "Usage is: %s <host> <port>\n", argv[0]);
        exit(2); 
    }

    struct sockaddr_in server_addr;
    struct hostent *hp;
    hp = gethostbyname(argv[1]);
    
    if(hp == (struct hostent *) 0){
        fprintf(stderr, "%s - unknown host, changing to 127.0.0.1\n", argv[1]);
        hp = gethostbyname("127.0.0.1");
    }
    
    server_addr.sin_family = AF_INET;
    memcpy((char *) &server_addr.sin_addr, (char *) hp->h_addr, hp->h_length);
    server_addr.sin_port = htons(atoi(argv[2]));
    return server_addr;
}

void connect_socket(int sock, struct sockaddr_in serv_addr){
    if (connect(sock, (struct sockaddr *) &serv_addr, sizeof serv_addr) == -1){
        fprintf(stderr, "Error while connecting\n");
        exit(3);
    };
}

void start_sending1(int sock){
    // task 1.1
    char data[] = "Hello its 1.1 task.";
    for (int i = 0; i < N_MESSAGES; i++)
    {
        if (send(sock, data, sizeof data, 0) == -1)
        {
            fprintf(stderr, "Error while writing on socket!\n");
            exit(4);
        }
    }
}

void start_sending2(int sock){
    // task 1.2
    char data[SIZE];
    int i = 1;
    while(1)
    {
        memset(data, 0, sizeof data);
        append_multiple_chars(data, 'a', pov(2, i - 1));
        printf("Sending %d of bytes!\n", pov(2, i - 1));    
        if (send(sock, data, pov(2, i - 1), 0) == -1)
        {
            fprintf(stderr, "Error while writing on socket!\n");
            exit(4);
        };
        i+=1;
    }
}

int main(int argc, char *argv[])
{
    struct sockaddr_in server;
    server = prepare_addr(argc, argv);
    int sock = create_socket_udp();
    connect_socket(sock, server);
    // start_sending1(sock);
    start_sending2(sock);
    close(sock);
    exit(0);
}