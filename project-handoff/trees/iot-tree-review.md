# Internet of Things: enriched tree for review

Status: needs your review. Original syllabus structure and source text are preserved. Added distinctions and assessed aspects are proposed enrichment. Classification performance has not been tested.

Course: 2301306A | Syllabus: KKW-AIDS-2023

## Review decisions needed

- **Service and IoT level specification:** Does the garbled phrase represent separate service-specification and IoT-level-specification steps? Confirm against faculty material before approving the proposed aspects.
- **Working with accelerometers:** Does printed "accelerators" mean accelerometers? Current enrichment is provisional; retain original wording as evidence.
- **Introduction to cloud storage models:** Which cloud storage models are taught? Do not substitute service models or invent the expected answer.
- **Security model for IoT:** Which security model is intended by the course? A layered model is an example, not established by the source.
- **Threat modeling:** Is STRIDE explicitly taught? Keep it as a supporting example rather than an obligatory method.
- **Amazon Web Services for IoT:** Which historical/current AWS services are taught? Do not require all services inherited from the original enrichment.
- **Xively cloud for IoT:** Which syllabus-era Xively features are assessed? No current product-availability assertion is made.
- **SkyNet IoT messaging platform:** Confirm the exact SkyNet platform/version intended by the syllabus and teaching notes.
- **BeagleBoard and other IoT devices:** BeagleBoard and BeagleBone are related board families, not exact synonyms. Confirm the actual boards covered.
- **IoT protocols (physical design overview):** MQTT, CoAP, XMPP and AMQP were inferred by prior enrichment; confirm which are taught under the broad Unit I entry.

## How to read this tree

Descriptions identify the topic. Boundaries separate nearby concepts. Distinction notes do not imply A, B or C. Supporting examples are optional context, not requirements for every answer. Every enrichment remains needs-review.

## Introduction to IoT and its Platforms Design Methodology

ID: `2301306A/u1`

**Original syllabus:** Unit I Introduction to IoT and its Platforms Design

Hours: 9; outcomes: CO1.

### Definition and characteristics of IoT

ID: `2301306A/u1/definition`

**Original syllabus:** Definition and characteristics of IoT

What IoT is and its defining characteristics.

**Scope:** Meaning and defining properties of IoT.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** definition and characteristics of IoT

**Related terms, not aliases:** [{"term": "definition of IoT", "relation": "partial_aspect"}, {"term": "characteristics of IoT", "relation": "partial_aspect"}]

**Reference points:** dynamic and self-adapting; self-configuring; interoperable protocols; unique identity

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Aspect: Definition.** Meaning of IoT.
- **Aspect: Characteristics.** Properties of IoT systems; not interchangeable with definition alone.
- **Compared with Applications of IoT:** Definition and characteristics of IoT: Meaning and defining properties of IoT. Applications of IoT: Use cases and application domains. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT enabling technologies:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT enabling technologies: Supporting technologies that make IoT systems possible. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT levels and deployment templates:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT issues and challenges:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.

### Applications of IoT

ID: `2301306A/u1/applications`

**Original syllabus:** Applications

IoT application domains.

**Scope:** Use cases and application domains.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot applications, applications of iot

**Reference points:** home automation; smart cities; healthcare; agriculture; industry

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Definition and characteristics of IoT:** Definition and characteristics of IoT: Meaning and defining properties of IoT. Applications of IoT: Use cases and application domains. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT enabling technologies:** Applications of IoT: Use cases and application domains. IoT enabling technologies: Supporting technologies that make IoT systems possible. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT levels and deployment templates:** Applications of IoT: Use cases and application domains. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT issues and challenges:** Applications of IoT: Use cases and application domains. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.

### Physical design of IoT

ID: `2301306A/u1/physical-design`

**Original syllabus:** Physical design of IoT

The things and protocols that make up an IoT system physically.

**Scope:** Devices and communication technologies composing the physical system.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** physical design of iot

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Logical design of IoT:** Physical design of IoT: Devices and communication technologies composing the physical system. Logical design of IoT: Functional organization and communication abstractions. Shared family membership alone does not establish assessed overlap.

### Things of IoT

ID: `2301306A/u1/physical-design/things`

**Original syllabus:** Things of IoT

IoT devices: sensing, actuation and their interfaces.

**Scope:** IoT devices: sensing, actuation and their interfaces.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** things in iot, iot devices

**Reference points:** unique identity; sensing and actuation; device interfaces

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### IoT protocols (physical design overview)

ID: `2301306A/u1/physical-design/protocols`

**Original syllabus:** IoT Protocols

The IoT protocol stack by layer at overview level.

**Scope:** The IoT protocol stack by layer at overview level.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** iot protocol stack

**Reference points:** link layer; network layer; transport layer; application layer: http coap mqtt xmpp amqp

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Review needed:** MQTT, CoAP, XMPP and AMQP were inferred by prior enrichment; confirm which are taught under the broad Unit I entry.

### Logical design of IoT

ID: `2301306A/u1/logical-design`

**Original syllabus:** Logical design of IoT

Abstract view: functional blocks, communication models and APIs.

**Scope:** Functional organization and communication abstractions.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** logical design of iot

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Physical design of IoT:** Physical design of IoT: Devices and communication technologies composing the physical system. Logical design of IoT: Functional organization and communication abstractions. Shared family membership alone does not establish assessed overlap.

### IoT functional blocks

ID: `2301306A/u1/logical-design/functional-blocks`

**Original syllabus:** IoT functional blocks

Device, communication, services, management, security and application blocks.

**Scope:** Functional responsibilities such as communication, management and services.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** functional blocks of iot

**Reference points:** device; communication; services; management; security; application

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with IoT communication models:** IoT functional blocks: Functional responsibilities such as communication, management and services. IoT communication models: Interaction patterns such as request/response and publish/subscribe. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT communication APIs:** IoT functional blocks: Functional responsibilities such as communication, management and services. IoT communication APIs: Programming interfaces and communication mechanisms; distinguish REST-style interfaces and WebSocket use. Shared family membership alone does not establish assessed overlap.

### IoT communication models

ID: `2301306A/u1/logical-design/communication-models`

**Original syllabus:** IoT communication models

Request-response, publish-subscribe, push-pull and exclusive pair.

**Scope:** Interaction patterns such as request/response and publish/subscribe.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** communication models

**Reference points:** request-response; publish-subscribe; push-pull; exclusive pair

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Aspect: Request Response.** Assess this interaction pattern separately; distinguish it from a question asking for all communication models.
- **Aspect: Publish Subscribe.** Assess this interaction pattern separately; distinguish it from a question asking for all communication models.
- **Aspect: Push Pull.** Assess this interaction pattern separately; distinguish it from a question asking for all communication models.
- **Aspect: Exclusive Pair.** Assess this interaction pattern separately; distinguish it from a question asking for all communication models.
- **Compared with IoT functional blocks:** IoT functional blocks: Functional responsibilities such as communication, management and services. IoT communication models: Interaction patterns such as request/response and publish/subscribe. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT communication APIs:** IoT communication models: Interaction patterns such as request/response and publish/subscribe. IoT communication APIs: Programming interfaces and communication mechanisms; distinguish REST-style interfaces and WebSocket use. Shared family membership alone does not establish assessed overlap.

### IoT communication APIs

ID: `2301306A/u1/logical-design/communication-apis`

**Original syllabus:** IoT Communication APIs

REST-based and WebSocket-based communication APIs.

**Scope:** Programming interfaces and communication mechanisms; distinguish REST-style interfaces and WebSocket use.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** IoT communication APIs

**Related terms, not aliases:** [{"term": "REST API", "relation": "specific_api_style"}, {"term": "WebSocket API", "relation": "specific_mechanism"}]

**Reference points:** rest; websocket

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Aspect: REST-style API.** Resources and request/response interactions.
- **Aspect: WebSocket communication.** Persistent bidirectional communication; not an exact REST synonym.
- **Compared with IoT functional blocks:** IoT functional blocks: Functional responsibilities such as communication, management and services. IoT communication APIs: Programming interfaces and communication mechanisms; distinguish REST-style interfaces and WebSocket use. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT communication models:** IoT communication models: Interaction patterns such as request/response and publish/subscribe. IoT communication APIs: Programming interfaces and communication mechanisms; distinguish REST-style interfaces and WebSocket use. Shared family membership alone does not establish assessed overlap.

### IoT enabling technologies

ID: `2301306A/u1/enabling-technologies`

**Original syllabus:** IoT enabling technologies

Technologies behind IoT.

**Scope:** Supporting technologies that make IoT systems possible.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** enabling technologies

**Reference points:** wireless sensor networks; cloud computing; big data analytics; embedded systems

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Definition and characteristics of IoT:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT enabling technologies: Supporting technologies that make IoT systems possible. Shared family membership alone does not establish assessed overlap.
- **Compared with Applications of IoT:** Applications of IoT: Use cases and application domains. IoT enabling technologies: Supporting technologies that make IoT systems possible. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT levels and deployment templates:** IoT enabling technologies: Supporting technologies that make IoT systems possible. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT issues and challenges:** IoT enabling technologies: Supporting technologies that make IoT systems possible. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.

### IoT levels and deployment templates

ID: `2301306A/u1/levels`

**Original syllabus:** IoT levels and deployment templates

Levels 1 to 6 of IoT deployment with their components.

**Scope:** Deployment configurations and placement of processing/storage.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** IoT levels and deployment templates

**Related terms, not aliases:** [{"term": "IoT levels", "relation": "partial_aspect"}, {"term": "deployment templates", "relation": "partial_aspect"}]

**Reference points:** level 1 to level 6; local vs cloud analysis; coordinator node

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Definition and characteristics of IoT:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Applications of IoT:** Applications of IoT: Use cases and application domains. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT enabling technologies:** IoT enabling technologies: Supporting technologies that make IoT systems possible. IoT levels and deployment templates: Deployment configurations and placement of processing/storage. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT issues and challenges:** IoT levels and deployment templates: Deployment configurations and placement of processing/storage. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.

### IoT issues and challenges

ID: `2301306A/u1/issues`

**Original syllabus:** IoT Issues and Challenges

Open problems: security, privacy, interoperability, scalability.

**Scope:** Limitations and challenges; specify which challenge is assessed.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** challenges in iot, issues in iot

**Reference points:** privacy; interoperability; scalability; power

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Definition and characteristics of IoT:** Definition and characteristics of IoT: Meaning and defining properties of IoT. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.
- **Compared with Applications of IoT:** Applications of IoT: Use cases and application domains. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT enabling technologies:** IoT enabling technologies: Supporting technologies that make IoT systems possible. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.
- **Compared with IoT levels and deployment templates:** IoT levels and deployment templates: Deployment configurations and placement of processing/storage. IoT issues and challenges: Limitations and challenges; specify which challenge is assessed. Shared family membership alone does not establish assessed overlap.

### IoT platform design methodology

ID: `2301306A/u1/design-methodology`

**Original syllabus:** IoT Platform Design Methodology:

A staged methodology for specifying and implementing an IoT system. The printed service/level phrase is ambiguous; the exact decomposition requires faculty confirmation.

**Scope:** A staged methodology for specifying and implementing an IoT system. The printed service/level phrase is ambiguous; the exact decomposition requires faculty confirmation.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** iot design methodology, iot platform design methodology

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Purpose and requirement specification

ID: `2301306A/u1/design-methodology/purpose`

**Original syllabus:** Purpose and requirement specification

Defining system purpose, behaviour and requirements.

**Scope:** Goals, intended behavior and requirements.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** purpose and requirements

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Process specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Process specification: Activities and use cases needed to meet the purpose. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Domain model specification: Domain entities and their conceptual relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Purpose and requirement specification: Goals, intended behavior and requirements. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Purpose and requirement specification: Goals, intended behavior and requirements. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Process specification

ID: `2301306A/u1/design-methodology/process`

**Original syllabus:** Process specification

Use cases derived from the purpose.

**Scope:** Activities and use cases needed to meet the purpose.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** process specification

**Reference points:** use cases

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Process specification: Activities and use cases needed to meet the purpose. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Process specification: Activities and use cases needed to meet the purpose. Domain model specification: Domain entities and their conceptual relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Process specification: Activities and use cases needed to meet the purpose. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Process specification: Activities and use cases needed to meet the purpose. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Process specification: Activities and use cases needed to meet the purpose. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Process specification: Activities and use cases needed to meet the purpose. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Process specification: Activities and use cases needed to meet the purpose. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Process specification: Activities and use cases needed to meet the purpose. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Domain model specification

ID: `2301306A/u1/design-methodology/domain-model`

**Original syllabus:** Domain model specification

Main concepts, entities and objects of the domain.

**Scope:** Domain entities and their conceptual relationships.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** domain model

**Reference points:** physical entity; virtual entity; device; resource; service

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Domain model specification: Domain entities and their conceptual relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Domain model specification: Domain entities and their conceptual relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Domain model specification: Domain entities and their conceptual relationships. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Domain model specification: Domain entities and their conceptual relationships. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Domain model specification: Domain entities and their conceptual relationships. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Domain model specification: Domain entities and their conceptual relationships. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Domain model specification: Domain entities and their conceptual relationships. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Domain model specification: Domain entities and their conceptual relationships. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Information model specification

ID: `2301306A/u1/design-methodology/information-model`

**Original syllabus:** Information model specification

Structure of information: attributes and relations of virtual entities.

**Scope:** Information attributes, representation and relationships.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** information model

**Reference points:** virtual entity attributes; relations

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Information model specification: Information attributes, representation and relationships. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Information model specification: Information attributes, representation and relationships. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Information model specification: Information attributes, representation and relationships. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Information model specification: Information attributes, representation and relationships. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Information model specification: Information attributes, representation and relationships. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Information model specification: Information attributes, representation and relationships. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Service and IoT level specification

ID: `2301306A/u1/design-methodology/service`

**Original syllabus:** Service specifications level specification

Services of the system and the chosen IoT deployment level.

**Scope:** Service interfaces and deployment-level choice; printed combined phrase remains uncertain.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** service and IoT level specification

**Related terms, not aliases:** [{"term": "service specification", "relation": "partial_aspect_pending_interpretation"}, {"term": "IoT level specification", "relation": "partial_aspect_pending_interpretation"}]

**Reference points:** service types; inputs outputs endpoints; deployment level

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Aspect: Service specification.** Specify services, inputs, outputs and interfaces; provisional decomposition.
- **Aspect: IoT-level specification.** Select a deployment level; provisional interpretation of garbled source.
- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Information model specification: Information attributes, representation and relationships. Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Does the garbled phrase represent separate service-specification and IoT-level-specification steps? Confirm against faculty material before approving the proposed aspects.

### Functional view specification

ID: `2301306A/u1/design-methodology/functional-view`

**Original syllabus:** Functional view specification

Mapping functional groups to the domain and information models.

**Scope:** Functional groups and their responsibilities.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** functional view

**Reference points:** functional groups

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Information model specification: Information attributes, representation and relationships. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Functional view specification: Functional groups and their responsibilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Functional view specification: Functional groups and their responsibilities. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Functional view specification: Functional groups and their responsibilities. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Functional view specification: Functional groups and their responsibilities. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Operational view specification

ID: `2301306A/u1/design-methodology/operational-view`

**Original syllabus:** Operational view specification

Deployment and operation options: hosting, storage, devices.

**Scope:** Deployment/operating choices for devices, services and storage.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** operational view

**Reference points:** service hosting; storage options; device options

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Information model specification: Information attributes, representation and relationships. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Functional view specification: Functional groups and their responsibilities. Operational view specification: Deployment/operating choices for devices, services and storage. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Operational view specification: Deployment/operating choices for devices, services and storage. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Operational view specification: Deployment/operating choices for devices, services and storage. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Device and component integration

ID: `2301306A/u1/design-methodology/integration`

**Original syllabus:** Device and component integration

Integrating devices and components into the system.

**Scope:** Connect and integrate selected devices and components.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** device integration

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Information model specification: Information attributes, representation and relationships. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Functional view specification: Functional groups and their responsibilities. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Operational view specification: Deployment/operating choices for devices, services and storage. Device and component integration: Connect and integrate selected devices and components. Shared family membership alone does not establish assessed overlap.
- **Compared with Application development:** Device and component integration: Connect and integrate selected devices and components. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

### Application development

ID: `2301306A/u1/design-methodology/app-development`

**Original syllabus:** Application development

Developing the IoT application.

**Scope:** Implement application behavior using the specified design.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot application development

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Purpose and requirement specification:** Purpose and requirement specification: Goals, intended behavior and requirements. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Process specification:** Process specification: Activities and use cases needed to meet the purpose. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Domain model specification:** Domain model specification: Domain entities and their conceptual relationships. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Information model specification:** Information model specification: Information attributes, representation and relationships. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Service and IoT level specification:** Service and IoT level specification: Service interfaces and deployment-level choice; printed combined phrase remains uncertain. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Functional view specification:** Functional view specification: Functional groups and their responsibilities. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Operational view specification:** Operational view specification: Deployment/operating choices for devices, services and storage. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.
- **Compared with Device and component integration:** Device and component integration: Connect and integrate selected devices and components. Application development: Implement application behavior using the specified design. Shared family membership alone does not establish assessed overlap.

## IoT Physical Devices and Programming Raspberry Pi with Python

ID: `2301306A/u2`

**Original syllabus:** Unit II IoT Physical Devices and Programming (07 hrs) CO2

Hours: 7; outcomes: CO2.

### Basic building blocks of an IoT device

ID: `2301306A/u2/building-blocks`

**Original syllabus:** Basic building blocks of IoT device

Sensing, actuation, communication and analysis/processing.

**Scope:** Roles of sensing, actuation, processing and communication in a device.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** building blocks of iot device

**Reference points:** sensing; actuation; communication; processing

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Sensors and actuators:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Shared family membership alone does not establish assessed overlap.
- **Compared with Connectivity technologies:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Connectivity technologies: Technology choices for connecting devices. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi interfaces:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with BeagleBoard and other IoT devices:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.

### Sensors and actuators

ID: `2301306A/u2/sensors-actuators`

**Original syllabus:** Sensors and actuators

Devices that measure the world and devices that act on it.

**Scope:** Measurement versus physical action; keep the selected device role explicit.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** sensors and actuators

**Related terms, not aliases:** [{"term": "sensors", "relation": "partial_aspect"}, {"term": "actuators", "relation": "partial_aspect"}]

**Reference points:** types of sensors; types of actuators; analog vs digital sensors

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Aspect: Sensors.** Convert physical conditions into measurements.
- **Aspect: Actuators.** Convert control signals into physical action.
- **Compared with Basic building blocks of an IoT device:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Shared family membership alone does not establish assessed overlap.
- **Compared with Connectivity technologies:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Connectivity technologies: Technology choices for connecting devices. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi interfaces:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with BeagleBoard and other IoT devices:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.

### Connectivity technologies

ID: `2301306A/u2/connectivity`

**Original syllabus:** Connectivity technologies

How devices connect: Wi-Fi, Bluetooth, cellular and more.

**Scope:** Technology choices for connecting devices.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot connectivity

**Reference points:** wi-fi; bluetooth; cellular; zigbee

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Basic building blocks of an IoT device:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Connectivity technologies: Technology choices for connecting devices. Shared family membership alone does not establish assessed overlap.
- **Compared with Sensors and actuators:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Connectivity technologies: Technology choices for connecting devices. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi:** Connectivity technologies: Technology choices for connecting devices. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi interfaces:** Connectivity technologies: Technology choices for connecting devices. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with BeagleBoard and other IoT devices:** Connectivity technologies: Technology choices for connecting devices. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.

### Raspberry Pi

ID: `2301306A/u2/raspberry-pi`

**Original syllabus:** Exemplary device: Raspberry Pi

The Raspberry Pi board and its specifications.

**Scope:** Board architecture and capabilities; hardware version matters.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** raspberry pi

**Reference points:** board specifications; raspbian; gpio

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Basic building blocks of an IoT device:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Sensors and actuators:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Connectivity technologies:** Connectivity technologies: Technology choices for connecting devices. Raspberry Pi: Board architecture and capabilities; hardware version matters. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi interfaces:** Raspberry Pi: Board architecture and capabilities; hardware version matters. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with BeagleBoard and other IoT devices:** Raspberry Pi: Board architecture and capabilities; hardware version matters. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.

### Raspberry Pi interfaces

ID: `2301306A/u2/rpi-interfaces`

**Original syllabus:** Raspberry Pi interfaces

Serial, SPI and I2C interfaces on the Pi.

**Scope:** Specific interface signals, connections and communication.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** raspberry pi interfaces

**Reference points:** serial; spi; i2c; gpio pins

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Basic building blocks of an IoT device:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with Sensors and actuators:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with Connectivity technologies:** Connectivity technologies: Technology choices for connecting devices. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi:** Raspberry Pi: Board architecture and capabilities; hardware version matters. Raspberry Pi interfaces: Specific interface signals, connections and communication. Shared family membership alone does not establish assessed overlap.
- **Compared with BeagleBoard and other IoT devices:** Raspberry Pi interfaces: Specific interface signals, connections and communication. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.

### BeagleBoard and other IoT devices

ID: `2301306A/u2/other-devices`

**Original syllabus:** Beagle board and Other IoT Devices

Other IoT boards such as BeagleBone, Arduino and pcDuino.

**Scope:** Other boards; names and capabilities are board-specific, not exact aliases.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** beagle board, other iot devices

**Reference points:** beaglebone; arduino; pcduino

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Basic building blocks of an IoT device:** Basic building blocks of an IoT device: Roles of sensing, actuation, processing and communication in a device. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.
- **Compared with Sensors and actuators:** Sensors and actuators: Measurement versus physical action; keep the selected device role explicit. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.
- **Compared with Connectivity technologies:** Connectivity technologies: Technology choices for connecting devices. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi:** Raspberry Pi: Board architecture and capabilities; hardware version matters. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.
- **Compared with Raspberry Pi interfaces:** Raspberry Pi interfaces: Specific interface signals, connections and communication. BeagleBoard and other IoT devices: Other boards; names and capabilities are board-specific, not exact aliases. Shared family membership alone does not establish assessed overlap.
- **Review needed:** BeagleBoard and BeagleBone are related board families, not exact synonyms. Confirm the actual boards covered.

### Programming Raspberry Pi with Python

ID: `2301306A/u2/programming`

**Original syllabus:** Programming Raspberry Pi with Python:

Python programs for Raspberry Pi I/O, sensors, displays and cloud.

**Scope:** Python programs for Raspberry Pi I/O, sensors, displays and cloud.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** raspberry pi python programming

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Digital and analog input/output

ID: `2301306A/u2/programming/digital-analog-io`

**Original syllabus:** Working with digital and analog input output

Reading switches, driving LEDs and using ADCs.

**Scope:** Read/write digital signals and interface analog conversion hardware as specified.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** gpio programming

**Reference points:** gpio read and write; led and switch; adc

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Aspect: Digital I/O.** Discrete input/output states.
- **Aspect: Analog interfacing.** Analog readings/outputs need the specified conversion hardware; do not assume native analog input on every Pi.
- **Compared with Retrieving data with sensors:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Retrieving data with sensors: Acquire and process readings from a specified sensor. Shared family membership alone does not establish assessed overlap.
- **Compared with Working with accelerometers:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Shared family membership alone does not establish assessed overlap.
- **Compared with Temperature sensor:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Displaying information and acting with LCD and servo motors:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Publishing data to the cloud with PubNub:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.

### Retrieving data with sensors

ID: `2301306A/u2/programming/sensor-data`

**Original syllabus:** Retrieving data from the real world with sensors

Reading real-world data from sensors in Python.

**Scope:** Acquire and process readings from a specified sensor.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** reading sensors

**Reference points:** reading sensor values; polling

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Digital and analog input/output:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Retrieving data with sensors: Acquire and process readings from a specified sensor. Shared family membership alone does not establish assessed overlap.
- **Compared with Working with accelerometers:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Shared family membership alone does not establish assessed overlap.
- **Compared with Temperature sensor:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Displaying information and acting with LCD and servo motors:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Publishing data to the cloud with PubNub:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.

### Working with accelerometers

ID: `2301306A/u2/programming/accelerometers`

**Original syllabus:** Working with accelerators

Reading motion data from accelerometers.

**Scope:** Read acceleration/motion values; interpretation of the printed word remains pending.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** accelerometer

**Reference points:** acceleration axes; i2c accelerometer

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Digital and analog input/output:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Shared family membership alone does not establish assessed overlap.
- **Compared with Retrieving data with sensors:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Shared family membership alone does not establish assessed overlap.
- **Compared with Temperature sensor:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Displaying information and acting with LCD and servo motors:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Publishing data to the cloud with PubNub:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Does printed "accelerators" mean accelerometers? Current enrichment is provisional; retain original wording as evidence.

### Temperature sensor

ID: `2301306A/u2/programming/temperature-sensor`

**Original syllabus:** Temperature sensor

Reading temperature sensors such as DHT11/DS18B20.

**Scope:** Acquire temperature using the specified sensor and interface.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** temperature sensor

**Reference points:** dht11; ds18b20

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Digital and analog input/output:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Retrieving data with sensors:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Working with accelerometers:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Temperature sensor: Acquire temperature using the specified sensor and interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Displaying information and acting with LCD and servo motors:** Temperature sensor: Acquire temperature using the specified sensor and interface. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Publishing data to the cloud with PubNub:** Temperature sensor: Acquire temperature using the specified sensor and interface. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.

### Displaying information and acting with LCD and servo motors

ID: `2301306A/u2/programming/lcd-servo`

**Original syllabus:** Displaying information and performing action using LCD and Servo motors

Output to LCD displays and controlling servo motors.

**Scope:** Display information or drive a servo; preserve which output is requested.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** LCD and servo interfacing

**Related terms, not aliases:** [{"term": "LCD with Raspberry Pi", "relation": "partial_aspect"}, {"term": "servo motor control", "relation": "partial_aspect"}]

**Reference points:** lcd display; servo motor; pwm

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Aspect: LCD output.** Display data through the specified LCD interface.
- **Aspect: Servo control.** Control angular position using the specified hardware and signals.
- **Compared with Digital and analog input/output:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Retrieving data with sensors:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Working with accelerometers:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Temperature sensor:** Temperature sensor: Acquire temperature using the specified sensor and interface. Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Shared family membership alone does not establish assessed overlap.
- **Compared with Publishing data to the cloud with PubNub:** Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.

### Publishing data to the cloud with PubNub

ID: `2301306A/u2/programming/cloud-publishing`

**Original syllabus:** Working with cloud publishing data to the cloud-Python pub nub

Sending sensor data to the cloud via PubNub.

**Scope:** Publish device data using the specified cloud messaging interface.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** pubnub, publishing data to cloud

**Reference points:** pubnub; publish-subscribe

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Digital and analog input/output:** Digital and analog input/output: Read/write digital signals and interface analog conversion hardware as specified. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Retrieving data with sensors:** Retrieving data with sensors: Acquire and process readings from a specified sensor. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Working with accelerometers:** Working with accelerometers: Read acceleration/motion values; interpretation of the printed word remains pending. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Temperature sensor:** Temperature sensor: Acquire temperature using the specified sensor and interface. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.
- **Compared with Displaying information and acting with LCD and servo motors:** Displaying information and acting with LCD and servo motors: Display information or drive a servo; preserve which output is requested. Publishing data to the cloud with PubNub: Publish device data using the specified cloud messaging interface. Shared family membership alone does not establish assessed overlap.

## IoT Protocols

ID: `2301306A/u3`

**Original syllabus:** Unit III IoT Protocols (07 hrs) CO3

Hours: 7; outcomes: CO3.

### Four pillars of IoT

ID: `2301306A/u3/four-pillars`

**Original syllabus:** Four pillars of IoT:

The four technology pillars IoT grew from.

**Scope:** The four technology pillars IoT grew from.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** four pillars of iot

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### M2M

ID: `2301306A/u3/four-pillars/m2m`

**Original syllabus:** M2M

Machine-to-machine communication.

**Scope:** Communication between machines; broad interaction category.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** machine to machine

**Reference points:** machine to machine; m2m vs iot

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Wireless sensor networks:** M2M: Communication between machines; broad interaction category. Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. Shared family membership alone does not establish assessed overlap.
- **Compared with SCADA:** M2M: Communication between machines; broad interaction category. SCADA: Supervisory monitoring, control and data acquisition. Shared family membership alone does not establish assessed overlap.
- **Compared with RFID:** M2M: Communication between machines; broad interaction category. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.

### Wireless sensor networks

ID: `2301306A/u3/four-pillars/wsn`

**Original syllabus:** WSN

Networks of wireless sensor nodes.

**Scope:** Networks of sensor nodes and their sensing/communication organization.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** wireless sensor network

**Reference points:** sensor nodes; sink; multi-hop

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with M2M:** M2M: Communication between machines; broad interaction category. Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. Shared family membership alone does not establish assessed overlap.
- **Compared with SCADA:** Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. SCADA: Supervisory monitoring, control and data acquisition. Shared family membership alone does not establish assessed overlap.
- **Compared with RFID:** Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.

### SCADA

ID: `2301306A/u3/four-pillars/scada`

**Original syllabus:** SCADA

Supervisory control and data acquisition in industry.

**Scope:** Supervisory monitoring, control and data acquisition.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** supervisory control and data acquisition

**Reference points:** rtu; plc; hmi

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with M2M:** M2M: Communication between machines; broad interaction category. SCADA: Supervisory monitoring, control and data acquisition. Shared family membership alone does not establish assessed overlap.
- **Compared with Wireless sensor networks:** Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. SCADA: Supervisory monitoring, control and data acquisition. Shared family membership alone does not establish assessed overlap.
- **Compared with RFID:** SCADA: Supervisory monitoring, control and data acquisition. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.

### RFID

ID: `2301306A/u3/four-pillars/rfid`

**Original syllabus:** RFID

Radio-frequency identification with tags and readers.

**Scope:** Identification through tags and readers.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** radio frequency identification

**Reference points:** tags and readers; passive and active tags

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with M2M:** M2M: Communication between machines; broad interaction category. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.
- **Compared with Wireless sensor networks:** Wireless sensor networks: Networks of sensor nodes and their sensing/communication organization. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.
- **Compared with SCADA:** SCADA: Supervisory monitoring, control and data acquisition. RFID: Identification through tags and readers. Shared family membership alone does not establish assessed overlap.

### Protocol standardization for IoT

ID: `2301306A/u3/standardization`

**Original syllabus:** Protocol Standardization for IoT:

Standardization problems and unified data standards.

**Scope:** Standardization problems and unified data standards.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** iot standardization

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Issues with IoT standardization

ID: `2301306A/u3/standardization/issues`

**Original syllabus:** Issues with

Why IoT standardization is hard.

**Scope:** Barriers to interoperability and standardization.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** standardization issues

**Reference points:** fragmented standards; interoperability

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Unified data standards:** Issues with IoT standardization: Barriers to interoperability and standardization. Unified data standards: Consistent data representation and exchange conventions. Shared family membership alone does not establish assessed overlap.

### Unified data standards

ID: `2301306A/u3/standardization/unified-data-standards`

**Original syllabus:** Unified Data Standards

Common data formats and platforms across IoT.

**Scope:** Consistent data representation and exchange conventions.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** unified data standards

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Issues with IoT standardization:** Issues with IoT standardization: Barriers to interoperability and standardization. Unified data standards: Consistent data representation and exchange conventions. Shared family membership alone does not establish assessed overlap.

### IoT protocols

ID: `2301306A/u3/protocols`

**Original syllabus:** IoT Protocols:

Specific IoT communication protocols.

**Scope:** Specific IoT communication protocols.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** iot protocols

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### IEEE 802.15.4

ID: `2301306A/u3/protocols/ieee-802-15-4`

**Original syllabus:** IEEE 802.15.4

Low-rate wireless PAN standard underlying Zigbee and 6LoWPAN.

**Scope:** Low-rate wireless physical and MAC layers.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** ieee 802.15.4

**Reference points:** low rate wpan; phy and mac layers

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with Zigbee:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. Zigbee: A networking/application ecosystem built on IEEE 802.15.4. Shared family membership alone does not establish assessed overlap.
- **Compared with 6LoWPAN:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. Shared family membership alone does not establish assessed overlap.
- **Compared with LoRa:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.

### BACnet

ID: `2301306A/u3/protocols/bacnet`

**Original syllabus:** BACNet

Building automation and control networks protocol.

**Scope:** Building-automation communication with objects and services.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** bacnet

**Reference points:** building automation; objects and services

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with Modbus:** BACnet: Building-automation communication with objects and services. Modbus: Industrial data access through protocol-specific functions and a data model. Shared family membership alone does not establish assessed overlap.
- **Compared with KNX:** BACnet: Building-automation communication with objects and services. KNX: Home/building automation communication and interoperability. Shared family membership alone does not establish assessed overlap.

### Modbus

ID: `2301306A/u3/protocols/modbus`

**Original syllabus:** Modbus

Industrial communication protocol with a data model and request/response operations. Distinguish serial variants from Modbus TCP; transport and version details must follow the question.

**Scope:** Industrial data access through protocol-specific functions and a data model.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** modbus

**Reference points:** master slave; rtu and tcp modes; registers

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with BACnet:** BACnet: Building-automation communication with objects and services. Modbus: Industrial data access through protocol-specific functions and a data model. Shared family membership alone does not establish assessed overlap.
- **Compared with KNX:** Modbus: Industrial data access through protocol-specific functions and a data model. KNX: Home/building automation communication and interoperability. Shared family membership alone does not establish assessed overlap.

### KNX

ID: `2301306A/u3/protocols/knx`

**Original syllabus:** KNX

Building and home automation standard.

**Scope:** Home/building automation communication and interoperability.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** knx

**Reference points:** home and building automation

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with BACnet:** BACnet: Building-automation communication with objects and services. KNX: Home/building automation communication and interoperability. Shared family membership alone does not establish assessed overlap.
- **Compared with Modbus:** Modbus: Industrial data access through protocol-specific functions and a data model. KNX: Home/building automation communication and interoperability. Shared family membership alone does not establish assessed overlap.

### Zigbee

ID: `2301306A/u3/protocols/zigbee`

**Original syllabus:** Zigbee

Low-power mesh networking on IEEE 802.15.4.

**Scope:** A networking/application ecosystem built on IEEE 802.15.4.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** zigbee

**Reference points:** coordinator router end device; mesh; low power

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with IEEE 802.15.4:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. Zigbee: A networking/application ecosystem built on IEEE 802.15.4. Shared family membership alone does not establish assessed overlap.
- **Compared with 6LoWPAN:** Zigbee: A networking/application ecosystem built on IEEE 802.15.4. 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. Shared family membership alone does not establish assessed overlap.
- **Compared with LoRa:** Zigbee: A networking/application ecosystem built on IEEE 802.15.4. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.

### 6LoWPAN

ID: `2301306A/u3/protocols/6lowpan`

**Original syllabus:** 6LoWPAN

IPv6 over low-power wireless networks with header compression.

**Scope:** Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** 6lowpan

**Reference points:** ipv6 over 802.15.4; header compression; fragmentation

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with IEEE 802.15.4:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. Shared family membership alone does not establish assessed overlap.
- **Compared with Zigbee:** Zigbee: A networking/application ecosystem built on IEEE 802.15.4. 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. Shared family membership alone does not establish assessed overlap.
- **Compared with LoRa:** 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.

### LoRa

ID: `2301306A/u3/protocols/lora`

**Original syllabus:** LoRa

LoRa is a low-power, long-range radio physical-layer technology. LoRaWAN specifies networking behavior using LoRa; the two terms are related but not interchangeable.

**Scope:** Long-range low-power radio physical layer; distinguish LoRaWAN.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** LoRa

**Related terms, not aliases:** [{"term": "LoRaWAN", "relation": "network_protocol_using_lora_not_synonym"}]

**Reference points:** long-range low-power radio; physical-layer role; distinction from LoRaWAN

**Tasks to distinguish:** explain, compare, draw, design

**Preserve in the question:** protocol identity; layer; architecture; message/data flow; requested features; application context; specified protocol version

- **Compared with IEEE 802.15.4:** IEEE 802.15.4: Low-rate wireless physical and MAC layers. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.
- **Compared with Zigbee:** Zigbee: A networking/application ecosystem built on IEEE 802.15.4. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.
- **Compared with 6LoWPAN:** 6LoWPAN: Adapt IPv6 packets for constrained low-power links; not the radio or a Zigbee synonym. LoRa: Long-range low-power radio physical layer; distinguish LoRaWAN. Shared family membership alone does not establish assessed overlap.

## IoT Security

ID: `2301306A/u4`

**Original syllabus:** Unit IV IoT Security (06 hrs) CO4

Hours: 6; outcomes: CO4.

### Vulnerabilities of IoT

ID: `2301306A/u4/vulnerabilities`

**Original syllabus:** Vulnerabilities of IoT

Weaknesses of IoT devices and networks.

**Scope:** Concrete weaknesses that may be exploited.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot vulnerabilities

**Reference points:** weak authentication; insecure firmware; unencrypted traffic

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Security requirements:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Security requirements: Security properties the system should satisfy. Shared family membership alone does not establish assessed overlap.
- **Compared with Challenges for secure IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Challenges for secure IoT: Constraints that make security difficult to achieve. Shared family membership alone does not establish assessed overlap.
- **Compared with Threat modeling:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Security model for IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.

### Security requirements

ID: `2301306A/u4/requirements`

**Original syllabus:** Security Requirements

What secure IoT must provide.

**Scope:** Security properties the system should satisfy.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot security requirements

**Reference points:** confidentiality; integrity; authentication; availability

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Vulnerabilities of IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Security requirements: Security properties the system should satisfy. Shared family membership alone does not establish assessed overlap.
- **Compared with Challenges for secure IoT:** Security requirements: Security properties the system should satisfy. Challenges for secure IoT: Constraints that make security difficult to achieve. Shared family membership alone does not establish assessed overlap.
- **Compared with Threat modeling:** Security requirements: Security properties the system should satisfy. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Security model for IoT:** Security requirements: Security properties the system should satisfy. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.

### Challenges for secure IoT

ID: `2301306A/u4/challenges`

**Original syllabus:** Challenges for Secure IoT

Why securing IoT is difficult.

**Scope:** Constraints that make security difficult to achieve.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot security challenges

**Reference points:** constrained devices; scale; heterogeneity

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Vulnerabilities of IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Challenges for secure IoT: Constraints that make security difficult to achieve. Shared family membership alone does not establish assessed overlap.
- **Compared with Security requirements:** Security requirements: Security properties the system should satisfy. Challenges for secure IoT: Constraints that make security difficult to achieve. Shared family membership alone does not establish assessed overlap.
- **Compared with Threat modeling:** Challenges for secure IoT: Constraints that make security difficult to achieve. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Security model for IoT:** Challenges for secure IoT: Constraints that make security difficult to achieve. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.

### Threat modeling

ID: `2301306A/u4/threat-modeling`

**Original syllabus:** Threat Modeling

Identifying assets, threats and mitigations.

**Scope:** Analyze assets, attackers, attack surfaces and threats.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** threat modelling, threat model

**Reference points:** stride; attack surface; assets

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Vulnerabilities of IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Security requirements:** Security requirements: Security properties the system should satisfy. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Challenges for secure IoT:** Challenges for secure IoT: Constraints that make security difficult to achieve. Threat modeling: Analyze assets, attackers, attack surfaces and threats. Shared family membership alone does not establish assessed overlap.
- **Compared with Security model for IoT:** Threat modeling: Analyze assets, attackers, attack surfaces and threats. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Is STRIDE explicitly taught? Keep it as a supporting example rather than an obligatory method.

### Key elements of IoT security

ID: `2301306A/u4/key-elements`

**Original syllabus:** Key elements of IoT Security:

The core security mechanisms for IoT.

**Scope:** The core security mechanisms for IoT.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** elements of iot security

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Identity establishment

ID: `2301306A/u4/key-elements/identity`

**Original syllabus:** Identity establishment

Establishing device and user identities.

**Scope:** Establish which entity is involved and its claimed identity.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** identity management

**Reference points:** device identity; certificates

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Access control:** Identity establishment: Establish which entity is involved and its claimed identity. Access control: Decide which actions an entity is authorized to perform. Shared family membership alone does not establish assessed overlap.
- **Compared with Data and message security:** Identity establishment: Establish which entity is involved and its claimed identity. Data and message security: Protect data confidentiality and integrity in the specified setting. Shared family membership alone does not establish assessed overlap.
- **Compared with Non-repudiation:** Identity establishment: Establish which entity is involved and its claimed identity. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Availability:** Identity establishment: Establish which entity is involved and its claimed identity. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.

### Access control

ID: `2301306A/u4/key-elements/access-control`

**Original syllabus:** Access control

Controlling who may access which resources.

**Scope:** Decide which actions an entity is authorized to perform.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** access control

**Reference points:** authorization; role based access

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Identity establishment:** Identity establishment: Establish which entity is involved and its claimed identity. Access control: Decide which actions an entity is authorized to perform. Shared family membership alone does not establish assessed overlap.
- **Compared with Data and message security:** Access control: Decide which actions an entity is authorized to perform. Data and message security: Protect data confidentiality and integrity in the specified setting. Shared family membership alone does not establish assessed overlap.
- **Compared with Non-repudiation:** Access control: Decide which actions an entity is authorized to perform. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Availability:** Access control: Decide which actions an entity is authorized to perform. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.

### Data and message security

ID: `2301306A/u4/key-elements/data-message`

**Original syllabus:** Data and message security

Protecting data in transit and at rest.

**Scope:** Protect data confidentiality and integrity in the specified setting.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** data security, message security

**Reference points:** encryption; integrity checks

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Identity establishment:** Identity establishment: Establish which entity is involved and its claimed identity. Data and message security: Protect data confidentiality and integrity in the specified setting. Shared family membership alone does not establish assessed overlap.
- **Compared with Access control:** Access control: Decide which actions an entity is authorized to perform. Data and message security: Protect data confidentiality and integrity in the specified setting. Shared family membership alone does not establish assessed overlap.
- **Compared with Non-repudiation:** Data and message security: Protect data confidentiality and integrity in the specified setting. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Availability:** Data and message security: Protect data confidentiality and integrity in the specified setting. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.

### Non-repudiation

ID: `2301306A/u4/key-elements/non-repudiation`

**Original syllabus:** Non-repudiation

Preventing parties denying their actions.

**Scope:** Provide evidence supporting attribution so an action cannot credibly be denied.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** non repudiation

**Reference points:** digital signatures; audit logs

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Identity establishment:** Identity establishment: Establish which entity is involved and its claimed identity. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Access control:** Access control: Decide which actions an entity is authorized to perform. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Data and message security:** Data and message security: Protect data confidentiality and integrity in the specified setting. Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Shared family membership alone does not establish assessed overlap.
- **Compared with Availability:** Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.

### Availability

ID: `2301306A/u4/key-elements/availability`

**Original syllabus:** availability

Keeping services available despite attacks.

**Scope:** Maintain access to required services despite faults or attacks.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** availability

**Reference points:** dos resistance; redundancy

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Identity establishment:** Identity establishment: Establish which entity is involved and its claimed identity. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.
- **Compared with Access control:** Access control: Decide which actions an entity is authorized to perform. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.
- **Compared with Data and message security:** Data and message security: Protect data confidentiality and integrity in the specified setting. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.
- **Compared with Non-repudiation:** Non-repudiation: Provide evidence supporting attribution so an action cannot credibly be denied. Availability: Maintain access to required services despite faults or attacks. Shared family membership alone does not establish assessed overlap.

### Security model for IoT

ID: `2301306A/u4/security-model`

**Original syllabus:** Security model for IoT

An overall security model for IoT systems.

**Scope:** Organize security assumptions, responsibilities and controls; identify the intended model.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** iot security model

**Reference points:** layered security model

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Vulnerabilities of IoT:** Vulnerabilities of IoT: Concrete weaknesses that may be exploited. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.
- **Compared with Security requirements:** Security requirements: Security properties the system should satisfy. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.
- **Compared with Challenges for secure IoT:** Challenges for secure IoT: Constraints that make security difficult to achieve. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.
- **Compared with Threat modeling:** Threat modeling: Analyze assets, attackers, attack surfaces and threats. Security model for IoT: Organize security assumptions, responsibilities and controls; identify the intended model. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Which security model is intended by the course? A layered model is an example, not established by the source.

## IoT Physical Servers and Cloud Offerings

ID: `2301306A/u5`

**Original syllabus:** Unit V IoT Physical servers and Cloud offering (07 hrs) CO5

Hours: 7; outcomes: CO5.

### Introduction to cloud storage models

ID: `2301306A/u5/cloud-storage-models`

**Original syllabus:** Introduction to Cloud Storage Models

Cloud storage models and their use for IoT data.

**Scope:** Organization and use of cloud storage; intended syllabus interpretation requires confirmation.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** cloud storage models

**Reference points:** cloud storage organization; storage requirements for IoT data

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Communication APIs (cloud):** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Communication APIs (cloud): Interfaces for communicating with cloud services. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Which cloud storage models are taught? Do not substitute service models or invent the expected answer.

### Communication APIs (cloud)

ID: `2301306A/u5/communication-api`

**Original syllabus:** Communication API

APIs for communicating with cloud IoT services.

**Scope:** Interfaces for communicating with cloud services.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** cloud communication api

**Reference points:** cloud apis

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Communication APIs (cloud): Interfaces for communicating with cloud services. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** Communication APIs (cloud): Interfaces for communicating with cloud services. WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** Communication APIs (cloud): Interfaces for communicating with cloud services. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** Communication APIs (cloud): Interfaces for communicating with cloud services. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** Communication APIs (cloud): Interfaces for communicating with cloud services. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** Communication APIs (cloud): Interfaces for communicating with cloud services. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.

### WAMP: AutobahnPython for IoT

ID: `2301306A/u5/wamp`

**Original syllabus:** WAMP: AutoBahn for IoT

Web Application Messaging Protocol with Autobahn.

**Scope:** Messaging with routed RPC and publish/subscribe, using the specified implementation.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** wamp, autobahn

**Reference points:** rpc and pub-sub; router; autobahn

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Shared family membership alone does not establish assessed overlap.
- **Compared with Communication APIs (cloud):** Communication APIs (cloud): Interfaces for communicating with cloud services. WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.

### Xively cloud for IoT

ID: `2301306A/u5/xively`

**Original syllabus:** Xively Cloud for IoT

Xively platform for IoT device data.

**Scope:** The syllabus-named Xively platform in its taught historical context.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** xively

**Reference points:** feeds; datastreams

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Communication APIs (cloud):** Communication APIs (cloud): Interfaces for communicating with cloud services. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Which syllabus-era Xively features are assessed? No current product-availability assertion is made.

### Python web application framework: Django

ID: `2301306A/u5/django`

**Original syllabus:** Python Web Application Framework: Djanjo

Building IoT web apps with Django.

**Scope:** A Python web framework for implementing applications.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** django

**Reference points:** model view template; django project and app

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Communication APIs (cloud):** Communication APIs (cloud): Interfaces for communicating with cloud services. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Python web application framework: Django: A Python web framework for implementing applications. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** Python web application framework: Django: A Python web framework for implementing applications. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** Python web application framework: Django: A Python web framework for implementing applications. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.

### Amazon Web Services for IoT

ID: `2301306A/u5/aws`

**Original syllabus:** Amzon Web Services for IoT

AWS services used for IoT.

**Scope:** The specified AWS services and their role in an IoT solution.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** aws for iot, amazon web services

**Reference points:** ec2; s3; dynamodb; aws iot

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with Communication APIs (cloud):** Communication APIs (cloud): Interfaces for communicating with cloud services. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** Python web application framework: Django: A Python web framework for implementing applications. Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. Shared family membership alone does not establish assessed overlap.
- **Compared with SkyNet IoT messaging platform:** Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Which historical/current AWS services are taught? Do not require all services inherited from the original enrichment.

### SkyNet IoT messaging platform

ID: `2301306A/u5/skynet`

**Original syllabus:** SkyNet IoT Messaging Platform

Open messaging platform for IoT devices.

**Scope:** The syllabus-named SkyNet messaging platform in its taught historical context.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** skynet

**Reference points:** device registration; messaging api

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Introduction to cloud storage models:** Introduction to cloud storage models: Organization and use of cloud storage; intended syllabus interpretation requires confirmation. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Communication APIs (cloud):** Communication APIs (cloud): Interfaces for communicating with cloud services. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with WAMP: AutobahnPython for IoT:** WAMP: AutobahnPython for IoT: Messaging with routed RPC and publish/subscribe, using the specified implementation. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Xively cloud for IoT:** Xively cloud for IoT: The syllabus-named Xively platform in its taught historical context. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Python web application framework: Django:** Python web application framework: Django: A Python web framework for implementing applications. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Compared with Amazon Web Services for IoT:** Amazon Web Services for IoT: The specified AWS services and their role in an IoT solution. SkyNet IoT messaging platform: The syllabus-named SkyNet messaging platform in its taught historical context. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Confirm the exact SkyNet platform/version intended by the syllabus and teaching notes.

## Assumptions

- The original tree supplies the official outline; added aspects do not add official syllabus coverage.
- Exact exam question patterns have not been supplied here and are not inferred.
- Prior model-generated textbook details are retained as review material, not independently verified teaching requirements.
- No faculty-feedback learning or automatic ruling propagation is added.
