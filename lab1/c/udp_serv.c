#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#define SIZE 40000

// run by using ./udp_serv <port>

int create_socket_udp(){
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1){
        fprintf(stderr, "Error while creating socket\n");
        exit(1);
    }
    return sock;
}

void prepare_socket_address(struct sockaddr_in* sock_addr, int argc, char *argv[]){
    if(argc != 1 && argc != 2){
        fprintf(stderr, "Usage is: %s <port> or just %s\n", argv[0], argv[0]);
        exit(2); 
    }
    if(argc == 2){
        sock_addr->sin_port = htons(atoi(argv[1]));
    }
    else{
        printf("Port not specified, using random!\n");
        sock_addr->sin_port = 0;
    }
    sock_addr->sin_family = AF_INET;
    sock_addr->sin_addr.s_addr = INADDR_ANY;
    
}

void bind_socket(int sock, struct sockaddr_in* sock_addr){
    
    int res = bind(sock, (struct sockaddr*) sock_addr, sizeof(struct sockaddr_in));
    if (res == -1){
        fprintf(stderr, "Error while binding\n");
        exit(3);
    }
}

void get_server_port_info(int sock){
    struct sockaddr_in sock_addr_info;
    int size = sizeof(struct sockaddr_in);
    int res = getsockname(sock, (struct sockaddr*) &sock_addr_info, &size);
    if(res == -1){
        fprintf(stderr, "Error while getting socket name\n");
        exit(4);
    }
    printf("Server UDP at port: %d!\n", ntohs(sock_addr_info.sin_port));

}

void run_server_reading(int sock){
    char buf[SIZE];
    while(1){
        memset(buf, 0, SIZE);
        int res = recv(sock, buf, SIZE, 0);
        if(res == -1){
            fprintf(stderr, "Error while reading from client\n");
            exit(5);
        }
        // for 1.1
        // printf("Received %d bytes: %s\n", res, buf);     
        // for 1.2
        printf("Received %d bytes!\n", res);
    }
}

void main(int argc, char *argv[]){
    struct sockaddr_in sock_addr;
    int sock = create_socket_udp();
    prepare_socket_address(&sock_addr, argc, argv);
    bind_socket(sock, &sock_addr);
    get_server_port_info(sock);
    run_server_reading(sock);
    exit(0);
}