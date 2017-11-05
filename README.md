# Junosphere

Junosphere (https://www.junosphere.net) is Juniper's virtual training and experimentation platform. It supports the creation of virtual topologies of MX, PTX and other devives by using their virtual counterparts (i.e. vMX for MX).

This repository contains the topologies I used for learning Junos and Juniper networking. It also continas a tool script, which aims to simplify the usage of Junosphere by interacting with its API (see below). It currently supports:
* list topologies
* download fileset's (i.e. the structure and config files of a topology)
* upload new fileset (to-be-completed)
* list virtual machines

## Junosphere API

* User: https://junosphere.net/api/userService/users
* Bank: https://junosphere.net/api/bankService/banks
* Sandbox: https://junosphere.net/api/sandboxService/sandboxes
  * Active Topology: https://junosphere.net/api/sandboxService/sandboxes/{sandbox_id}/active
  * Virtual Machines: https://junosphere.net/api/sandboxService/sandboxes/{sandbox_id}/active/vmachines
* Topology: https://junosphere.net/api/topologyService/topologies
  * Download files: https://junosphere.net/api/topologyService/topologies/{topology_id}/fileset
