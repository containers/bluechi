#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "libhirte/common/opt.h"
#include "libhirte/log/log.h"

#include "agent.h"

const struct option options[] = { { ARG_HOST, required_argument, 0, ARG_HOST_SHORT },
                                  { ARG_PORT, required_argument, 0, ARG_PORT_SHORT },
                                  { ARG_NAME, required_argument, 0, ARG_NAME_SHORT },
                                  { ARG_CONFIG, required_argument, 0, ARG_CONFIG_SHORT },
                                  { ARG_HELP, no_argument, 0, ARG_HELP_SHORT },
                                  { NULL, 0, 0, '\0' } };

#define OPTIONS_STR ARG_PORT_SHORT_S ARG_HOST_SHORT_S ARG_HELP_SHORT_S ARG_CONFIG_SHORT_S ARG_NAME_SHORT_S

static const char *opt_port = 0;
static const char *opt_host = NULL;
static const char *opt_name = NULL;
static const char *opt_config = NULL;

static void usage(char *argv[]) {
        printf("Usage: %s [-H host] [-p port] [-c config] [-n name]\n", argv[0]);
}

static int get_opts(int argc, char *argv[]) {
        int opt = 0;

        while ((opt = getopt_long(argc, argv, OPTIONS_STR, options, NULL)) != -1) {
                switch (opt) {
                case ARG_HELP_SHORT:
                        usage(argv);
                        return 0;

                case ARG_NAME_SHORT:
                        opt_name = optarg;
                        break;

                case ARG_HOST_SHORT:
                        opt_host = optarg;
                        break;

                case ARG_CONFIG_SHORT:
                        opt_config = optarg;
                        break;

                case ARG_PORT_SHORT:
                        opt_port = optarg;
                        break;

                default:
                        fprintf(stderr, "Unsupported option %c\n", opt);
                        usage(argv);
                        return -EINVAL;
                }
        }

        return 0;
}

int main(int argc, char *argv[]) {
        int r = get_opts(argc, argv);
        if (r < 0) {
                return EXIT_FAILURE;
        }

        _cleanup_agent_ Agent *agent = agent_new();
        if (agent == NULL) {
                return EXIT_FAILURE;
        }

        /* First load config */
        if (opt_config) {
                if (!agent_parse_config(agent, opt_config)) {
                        return EXIT_FAILURE;
                }
        }

        /* Then override individual options */

        if (opt_port && !agent_set_port(agent, opt_port)) {
                return EXIT_FAILURE;
        }

        if (opt_host && !agent_set_host(agent, opt_host)) {
                return EXIT_FAILURE;
        }

        if (opt_name && !agent_set_name(agent, opt_name)) {
                return EXIT_FAILURE;
        }

        if (agent_start(agent)) {
                return EXIT_SUCCESS;
        }

        return EXIT_FAILURE;
}
