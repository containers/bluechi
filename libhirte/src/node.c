#include <stdio.h>

#include "../include/node.h"
#include "../include/peer-bus.h"
#include "./common/dbus.h"

Node *node_new(const NodeParams *params) {
        fprintf(stdout, "Creating Node...\n");

        int r = 0;
        _cleanup_sd_event_ sd_event *event = NULL;
        r = sd_event_default(&event);
        if (r < 0) {
                fprintf(stderr, "Failed to create event loop: %s\n", strerror(-r));
                return NULL;
        }

        char *orch_addr = assemble_tcp_address(params->orch_addr);
        if (orch_addr == NULL) {
                return NULL;
        }

        _cleanup_sd_bus_ sd_bus *peer_dbus = peer_bus_open(event, "peer-bus-to-orchestrator", orch_addr);
        if (peer_dbus == NULL) {
                fprintf(stderr, "Failed to open peer dbus\n");
                return false;
        }

        Node *n = malloc0(sizeof(Node));
        n->event_loop = steal_pointer(&event);
        n->orch_addr = orch_addr;
        n->peer_dbus = steal_pointer(&peer_dbus);

        return n;
}

void node_unrefp(Node **node) {
        fprintf(stdout, "Freeing allocated memory of Node...\n");
        if (node == NULL || (*node) == NULL) {
                return;
        }
        if ((*node)->event_loop != NULL) {
                fprintf(stdout, "Freeing allocated sd-event of Node...\n");
                sd_event_unrefp(&(*node)->event_loop);
        }
        if ((*node)->orch_addr != NULL) {
                fprintf(stdout, "Freeing allocated orch_addr of Node...\n");
                free((*node)->orch_addr);
        }
        if ((*node)->peer_dbus != NULL) {
                fprintf(stdout, "Freeing allocated peer dbus to Orchestrator...\n");
                sd_bus_unrefp(&(*node)->peer_dbus);
        }
        if ((*node)->user_dbus != NULL) {
                fprintf(stdout, "Freeing allocated dbus to local user dbus...\n");
                sd_bus_unrefp(&(*node)->user_dbus);
        }
        if ((*node)->systemd_dbus != NULL) {
                fprintf(stdout, "Freeing allocated dbus to local systemd dbus...\n");
                sd_bus_unrefp(&(*node)->systemd_dbus);
        }

        free(*node);
}

bool node_start(Node *node) {
        fprintf(stdout, "Starting Node...\n");

        if (node == NULL) {
                return false;
        }

        int r = 0;
        r = sd_event_loop(node->event_loop);
        if (r < 0) {
                fprintf(stderr, "Starting event loop failed: %s\n", strerror(-r));
                return false;
        }

        return true;
}

bool node_stop(const Node *node) {
        fprintf(stdout, "Stopping Node...\n");

        if (node == NULL) {
                return false;
        }

        return true;
}
