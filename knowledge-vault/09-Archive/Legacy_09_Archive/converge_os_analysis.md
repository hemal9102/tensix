---
title: "Converge OS - Landing Page Analysis"
type: "archive"
status: "archived"
project: "[[hemalshah_portfolio]]"
tags: ["archive", "converge-os", "analysis"]
created: 2026-07-26
updated: 2026-07-26
priority: "low"
owner: "Hemal Shah"
---

# Converge OS - Landing Page Analysis

## 1. Overview
The provided code is a single-page, highly interactive HTML/CSS/JS landing page for **Converge OS**. The company positions itself not as a traditional marketing agency, but as a **Revenue Operations (RevOps) and Systems Engineering** partner. Their core value proposition is finding and fixing "revenue leakage" by connecting disjointed marketing, sales, and delivery systems into one unified operational stream.

## 2. Key Personnel
- **Tirth Patel**: Founder & CEO
- **Manan Parmar**: Co-Founder & COO

## 3. Target Audience & Industries
The service is targeted at growth-stage, revenue-driven teams that have outgrown manual processes. Specific verticals mentioned include:
- B2B & SaaS
- Real Estate
- Healthcare
- Agencies

## 4. Core Offerings & Services
Converge OS operates in three main phases:
1. **Phase 1: Deep Diagnostic Audit** - Identifying exactly where leads and revenue are dropping off.
2. **Phase 2: Pipeline Engineering** - Connecting CRMs, automating handoffs, and building unified dashboards.
3. **Phase 3: Fractional RevOps** - Ongoing system management and optimization.

## 5. Notable Technical & Interactive Features
The landing page is technically sophisticated, utilizing vanilla JavaScript to drive several complex frontend features without heavy external libraries:
- **Revenue Leakage Calculator**: An interactive tool where users input monthly leads, client value, current close rate, and follow-up speed. The JS dynamically calculates estimated lost revenue and "recoverable" revenue, visually updating a sparkline chart.
- **Octagon Flow Diagram (The System)**: A scroll-driven, 3D-tilted SVG animation that visually demonstrates a broken pipeline (Marketing → Lead → Conversation, etc.) being "reconnected" as the user scrolls.
- **WhatsApp Integration**: The calculator data can be exported directly to a WhatsApp chat (number: `919213527202`) to book a diagnostic call.
- **Custom UI Details**: 
  - A custom magnetic cursor ring.
  - Scroll progress bar on the sticky navigation.
  - IntersectionObserver-based reveal animations for sections and counters.
  - Exit-intent popup offering a free diagnostic.
  - Currency conversion logic built into the calculator using external exchange rates.

## 6. Design Language
- **Theme**: Dark mode by default (`var(--bg): #0b1118`) with high-contrast, neon green accents (`var(--green): #00e57a`).
- **Typography**: Clean, modern sans-serif (Inter) with tight letter spacing for headings, giving it a premium tech/SaaS feel.
- **Assets**: Uses inline SVG icons (symbol definitions) to keep the footprint lightweight and scalable.

## Summary
The page is a well-engineered, high-converting B2B landing page. It heavily utilizes interactive data visualization (the calculator and the flow diagram) to prove its value proposition to potential clients before they even book a call.
