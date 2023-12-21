/* SPDX-License-Identifier: LGPL-2.1-or-later */
#pragma once

#include <inttypes.h>
#include <stdbool.h>

int create_tcp_socket(uint16_t port);
int accept_tcp_connection_request(int fd);

int fd_check_peercred(int fd);


typedef struct SocketOptions SocketOptions;

SocketOptions *socket_options_new();
int socket_options_set_tcp_keepidle(SocketOptions *opts, const char *keepidle_s);
int socket_options_set_tcp_keepintvl(SocketOptions *opts, const char *keepintvl_s);
int socket_options_set_tcp_keepcnt(SocketOptions *opts, const char *keepcnt_s);
int socket_options_set_ip_recverr(SocketOptions *opts, bool recverr);

int socket_set_options(int fd, SocketOptions *opts);
