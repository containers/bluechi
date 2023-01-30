#pragma once

#include "libhirte/common/common.h"

#include "types.h"

struct AgentRequest {
        int ref_count;
        Node *node;

        sd_bus_message *request_message;

        sd_bus_slot *slot;

        sd_bus_message *message;

        LIST_FIELDS(AgentRequest, outstanding_requests);
};

AgentRequest *agent_request_ref(AgentRequest *req);
void agent_request_unref(AgentRequest *req);
void agent_request_unrefp(AgentRequest **req);


struct Node {
        int ref_count;

        Manager *manager; /* weak ref */

        /* public bus api */
        sd_bus_slot *export_slot;

        /* internal bus api */
        sd_bus *agent_bus;
        sd_bus_slot *internal_manager_slot;
        sd_bus_slot *disconnect_slot;

        LIST_FIELDS(Node, nodes);

        char *name; /* NULL for not yet unregistred nodes */
        char *object_path;

        LIST_HEAD(AgentRequest, outstanding_requests);
};

Node *node_new(Manager *manager, const char *name);
Node *node_ref(Node *node);
void node_unref(Node *node);
void node_unrefp(Node **nodep);

bool node_export(Node *node);
bool node_has_agent(Node *node);
bool node_set_agent_bus(Node *node, sd_bus *bus);
void node_unset_agent_bus(Node *node);

#define _cleanup_node_ _cleanup_(node_unrefp)
#define _cleanup_agent_request_ _cleanup_(agent_request_unrefp)
