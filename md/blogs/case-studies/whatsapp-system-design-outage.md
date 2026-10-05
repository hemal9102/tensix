---
title: "WhatsApp System Design: Why It Lags Under Load | TENSIX"
url: https://www.tensix.in/blogs/case-studies/whatsapp-system-design-outage
description: "How WhatsApp delivers messages for billions of people, and the likely technical reasons it slows down after outages or big feature launches, explained."
---

[← Back to Blog](https://www.tensix.in/blogs)

System Design Erlang Outages

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# WhatsApp System Design: Why Was WhatsApp Lagging?

Published on July 30, 2026 • Newsjacking • System Design • Erlang

**In plain words**

WhatsApp delivers messages for billions of people using relatively few, very efficient servers built on Erlang, a language designed for phone networks. Each phone keeps a connection open, and the servers only pass along encrypted messages they cannot read. When something goes wrong, such as an outage, a new feature, or millions of phones reconnecting at once, messages can get stuck on one tick. The lesson for any business app is to plan for traffic spikes and recovery from day one; see [cloud and DevOps services](https://www.tensix.in/services/cloud-devops).

On July 30, 2026, many users reported that WhatsApp messages were slow to send in some areas. It was not a simple server crash. To see why this happens, it helps to know how WhatsApp is built: Erlang servers running on the BEAM virtual machine, its own version of the XMPP chat protocol, and new browser-calling features that were rolling out that week. Below, each part is explained, followed by likely causes. These are educated theories, not confirmed by Meta.

## 1. The Core: Erlang Servers and a Custom Chat Protocol

WhatsApp's servers are built on **Erlang** (a language first designed for telephone networks) and its **BEAM virtual machine**, using the Actor Model, where many small independent workers pass messages to each other.

- Each connected user maps to a lightweight, isolated Erlang process (costing ~2KB of memory).
- Initially built on **ejabberd** (an open-source XMPP server), WhatsApp heavily modified the XMPP protocol to strip out XML overhead, utilizing a proprietary, highly-compressed binary protocol.
- The system operates on an "async by default" philosophy, using Erlang's message-passing capabilities to bypass standard shared-memory lock contention.

## 2. Keeping Millions of Phones Connected at Once

WhatsApp engineers have publicly described single servers holding about 2 million open connections at the same time.

- **FreeBSD Kernel Tuning:** WhatsApp runs on FreeBSD rather than Linux due to its highly tunable network stack. They heavily manipulate kernel variables like `kern.ipc.maxsockets` and TCP hash sizes.
- **WebSocket / Long-Polling:** Persistent bidirectional connections allow the server to push messages directly to the client without HTTP overhead, managed efficiently by the BEAM preemptive scheduler.

## 3. Routing Messages and Keeping Them Private (Mnesia and Signal)

- **State Routing with Mnesia:** WhatsApp uses Erlang’s native distributed database, Mnesia, to rapidly map a user's ID to the specific server node they are connected to.
- **Signal Protocol:** Mnesia routes opaque binary blobs. The **Signal Protocol** (using the Double Ratchet Algorithm, X3DH, and Curve25519) operates entirely on the client edge. The backend never holds decryption keys; it merely queues and routes ciphertexts.

## 4. How Photos and Videos Travel Separately

- **Text:** Routed in real-time through Erlang chat servers and instantly purged from transient server memory upon delivery acknowledgement.
- **Media (Images/Video):** Media uses a decoupled architecture. The sender uploads encrypted media directly to a scalable object store (AWS S3/CDN) and receives a URL/hash pointer. This pointer (with the decryption key) is sent as a lightweight text message, keeping heavy binary blobs off the Erlang XMPP routers.

## 5. Why Was WhatsApp Lagging? Three Likely Theories

### 1. BEAM Scheduler Contention (Feature Rollout Bottleneck)

With the new browser-based calling update (July 28), the signaling channel is handling new WebRTC negotiation payloads (SDP offers/answers). If these payloads are larger or structurally unoptimized, they may cause excessive garbage collection (GC) pauses or message queue backups in the BEAM schedulers.

### 2. Mnesia Distributed Sync Delays (Post-Outage Hangover)

Following the major Meta outage on July 27, fragmented network partitions could have forced Mnesia into a split-brain recovery state. When Mnesia tables (which store user session mappings) are resyncing across global data centers, rapid lookups for routing messages can block, causing messages to hang on a single checkmark.

### 3. FreeBSD Socket Exhaustion from Retry Storms

Users experiencing lagging might be stuck in localized "retry storms" where mobile clients aggressively attempt to re-establish dropped WebSockets. This leads to localized TCP port exhaustion or TCP SYN floods on specific edge PoPs, maxing out `kern.ipc.maxsockets`.

## Sources

1. [Meta Outage (July 27)](https://www.sportskeeda.com/esports/news-is-whatsapp-down-today-july-27-2026)
2. [WhatsApp System Design Deep Dive (ByteByteGo)](https://bytebytego.com/courses/system-design-interview/design-a-chat-system)
3. [Scaling Erlang & FreeBSD to Millions of Connections](https://www.erlang-solutions.com/blog/scaling-to-millions-of-simultaneous-connections/)

← Previous post [Next: Why I Chose Automation Over a 9-to-5 →](https://www.tensix.in/blogs/why-i-chose-automation-over-a-9-to-5)
