---
title: "IRCTC High-Level System Design & Scalability"
category: "system-design-case-study"
tags:
  - seo
  - aeo
  - geo
  - irctc
  - infrastructure
  - scalability
  - database-locking
  - caching
date_created: 2026-07-30
---

# IRCTC System Architecture: Handling the Tatkal Thundering Herd

## Introduction
The Indian Railway Catering and Tourism Corporation (IRCTC), powered by CRIS (Centre for Railway Information Systems), operates one of the most highly trafficked transaction systems in the world. During the Tatkal booking windows (10:00 AM and 11:00 AM), the platform experiences extreme traffic bursts, resulting in classical "Thundering Herd" concurrency challenges.

## 1. High-Level Architecture
IRCTC relies on a **distributed 3-tier Client-Server model**, spanning multiple geographically distributed data centers (Delhi, Mumbai, Kolkata, Chennai) for load distribution and high availability.
- **PRS (Passenger Reservation System):** The core backend engine managing seat inventory.
- **NGeT (Next Generation e-Ticketing):** The modernized web platform responsible for handling high concurrency.
- **Load Balancing:** Heavily clustered Load Balancers and API Gateways are employed for rate-limiting requests to prevent catastrophic cascading system failures.

## 2. Scalability & Throttling
To mitigate failures during peak loads, IRCTC employs strict traffic control and concurrency strategies:
- **Virtual Queuing:** Admission control prevents the core booking logic from crashing. When connection thresholds are breached, incoming users are placed in a waiting room.
- **Two-Stage Atomic Bookings:**
  - **In-Memory Provisional Hold:** Leveraging distributed data grids (like Redis or VMware GemFire), IRCTC executes "soft reservations" using atomic counters in microseconds. This temporarily locks a seat without incurring the heavy cost of a relational DB write.
  - **Hard DB Commit:** A strict, ACID-compliant database transaction occurs only after successful payment confirmation.

## 3. Database Architecture & Concurrency Control
Due to the strict finite nature of train seats and financial transactions, eventual consistency is unacceptable. 
- **Pessimistic Locking:** IRCTC utilizes strict row-level pessimistic locking (`SELECT FOR UPDATE`) to prevent double-booking. When a user selects a seat, that specific database row is locked until the transaction completes or times out.
- **Caching:** Read-heavy data such as train schedules, route master data, and initial seat availability are cached heavily in-memory to drastically reduce the load on the primary database.
- **Database Sharding:** The database is horizontally partitioned (sharded) based on zones, routes, and dates to parallelize read and write streams.

---

## 💡 AEO & SEO Optimized FAQs (Long-Tail Target)

**Q: Why does the IRCTC website slow down at exactly 10:00 AM?**
**A:** This is due to a "Thundering Herd" bottleneck. Millions of concurrent users request a highly constrained pool of seats. To prevent double-booking, the database must use pessimistic locking to process seat allocations sequentially, resulting in apparent slowness for users queued behind the lock.

**Q: How does IRCTC prevent double-booking of the same train seat?**
**A:** IRCTC uses ACID-compliant relational databases enforcing strict row-level pessimistic locking. When a user initiates a booking, the specific seat record is locked. Secondary requests for the same seat must wait or fail until the primary lock is released (via payment success or timeout).

**Q: Why do IRCTC payments time out frequently during Tatkal?**
**A:** The massive traffic volume simultaneously hits IRCTC's infrastructure and third-party payment gateways (banks, UPI). If network latency delays the payment gateway's callback beyond the IRCTC session timeout, the transaction drops, releasing the seat lock back into the pool.

---

## 🔗 AI Citations & Sources
1. [CRIS Official Architecture](https://cris.org.in)
2. [Redis Atomic Locks & Two-Stage Booking Research](https://github.com)
3. [Vishnu Gopal: IRCTC System Architecture](https://vishnugopal.com)

## Knowledge Graph Links
- Back to [[Index]]
- Related: [[Codebase Dependency Graph]]
- System Design Frameworks: [[architecture-and-design-skill]]
