---
title: "How IRCTC Handles the Tatkal Rush: System Design | TENSIX"
url: https://www.tensix.in/blogs/case-studies/irctc-system-design-scalability
description: "Why IRCTC slows down at Tatkal time and how it stops two people booking the same seat: queues, caching, and database locks explained simply."
---

[← Back to Blog](https://www.tensix.in/blogs)

System Design Scalability India

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# IRCTC System Design: How It Handles the Tatkal Rush

Published on July 30, 2026 • Case Study • System Design • Scalability

**In plain words**

Every morning when Tatkal booking opens, a huge number of people try to book IRCTC tickets at the same moment, for very few seats. IRCTC copes by putting people in a virtual waiting room, holding a seat briefly while you pay, and locking each seat in the database so it is never sold twice. That is why the site feels slow at 10 AM, but rarely double-books. The same ideas help any Indian business that faces sale-day or festival rushes; see [cloud and DevOps services](https://www.tensix.in/services/cloud-devops) if your site needs to handle peaks.

IRCTC (the Indian Railway Catering and Tourism Corporation, with systems built by CRIS) runs one of the busiest booking systems in the world. When Tatkal booking opens at 10:00 AM and 11:00 AM, traffic jumps all at once. Engineers call this a **"thundering herd"**: a huge crowd hitting the same thing at the same moment.

## 1. The Big Picture

IRCTC uses a **3-tier client-server setup** (website, application servers, database) spread across data centres in Delhi, Mumbai, Kolkata, and Chennai, so the load is shared and one failure does not stop everything.

- **PRS (Passenger Reservation System):** The core backend engine managing seat inventory.
- **NGeT (Next Generation e-Ticketing):** The modernized web platform responsible for handling high concurrency.
- **Load Balancing:** Heavily clustered Load Balancers and API Gateways are employed for rate-limiting requests to prevent cascading system failures.

## 2. Controlling the Rush: Queues and Seat Holds

To avoid crashing at peak time, IRCTC controls how many people get in and how seats are held:

- **Virtual Queuing:** Admission control prevents the core booking logic from crashing. When connection thresholds are breached, incoming users are placed in a waiting room.
- **Two-Stage Atomic Bookings:**

  - **In-Memory Provisional Hold:** Leveraging distributed data grids (like Redis or VMware GemFire), IRCTC executes "soft reservations" using atomic counters in microseconds. This temporarily locks a seat without incurring the heavy cost of a relational DB write.
  - **Hard DB Commit:** A strict, ACID-compliant database transaction occurs only after successful payment confirmation.

## 3. Making Sure No Seat Is Sold Twice

A train has a fixed number of seats and every booking involves money, so the system cannot be "roughly right" (eventual consistency). Every seat count must be exact at all times.

- **Pessimistic Locking:** IRCTC utilizes strict row-level pessimistic locking (`SELECT FOR UPDATE`) to prevent double-booking. When a user selects a seat, that specific database row is locked until the transaction completes or times out.
- **Caching:** Read-heavy data such as train schedules, route master data, and initial seat availability are cached heavily in-memory.
- **Database Sharding:** The database is horizontally partitioned based on zones, routes, and dates to parallelize read and write streams.

## Common Questions

### Q: Why does the IRCTC website slow down at exactly 10:00 AM?

**A:** Because of a "thundering herd": a huge number of people try to book a small number of Tatkal seats at the same moment. To stop two people getting the same seat, the database locks each seat while it is being booked, so requests are handled one after another and the site feels slow.

### Q: How does IRCTC prevent double-booking of the same train seat?

**A:** It uses a reliable (ACID) relational database with row-level locks. When you start booking, that seat's record is locked. Anyone else trying for the same seat must wait or fail until the lock is released.

### Q: Why do IRCTC payments time out frequently during Tatkal?

**A:** The same rush hits IRCTC and the payment gateways at once. If the bank or gateway confirms the payment after your IRCTC session has timed out, the booking is dropped and the seat is released.

## Sources

1. [CRIS Official Architecture](https://cris.org.in)
2. [Vishnu Gopal: IRCTC System Architecture](https://vishnugopal.com)

← Previous post [Next: Why I Chose Automation Over a 9-to-5 →](https://www.tensix.in/blogs/why-i-chose-automation-over-a-9-to-5)
