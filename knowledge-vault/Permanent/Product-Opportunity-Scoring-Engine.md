---
title: Product Opportunity Scoring Engine
tags: [product-intelligence, scoring, algorithms, data-science, commerce]
updated: 2026-08-31
---

# Product Opportunity Scoring Engine

**Purpose:** Formulation and algorithmic breakdown of the Product Opportunity Score (POS) used to autonomously filter high-margin, high-velocity, low-risk commerce items.

**Summary:** Rather than humans manually scrolling social feeds for "winning products", the intelligence engine synthesizes real-time demand, trend velocity, unit margins, and AI discoverability into a composite index (0–100).

---

## 1. Score Composition & Weighting Matrix

| Dimension | Metric | Weight ($w_i$) | Description |
|---|---|:---:|---|
| **Demand Index** | Search Volume / Intent | 20% | Google Trends, Amazon BSR, Social search volume |
| **Trend Velocity** | $\Delta$ Acceleration | 15% | Rate of increase in search queries and mentions |
| **Gross Unit Margin** | $(P_{sell} - C_{landed}) / P_{sell}$ | 20% | Target minimum > 60% gross margin |
| **Supplier Reliability** | Fill rate & SLA history | 15% | Supplier historical defect and on-time shipment rate |
| **Shipping Velocity** | Average delivery days | 10% | Target < 4-7 days domestic/international |
| **Return Risk (Inverted)** | Defect / sizing variance | 10% | Low score if high breakage / complex sizing |
| **AI Discoverability** | Schema richness & entity match | 10% | Completeness of structured attributes for UCP/Shopping Graph |

---

## 2. Mathematical Formulation
$$\text{Opportunity Score} = \sum_{i=1}^{n} w_i \cdot S_i - \text{Penalties}$$

Where:
- $S_i \in [0, 100]$ is the normalized score for factor $i$.
- $\text{Penalties}$ apply for restricted categories (HAZMAT, trademark infringement, extreme fragility).

```text
Example Evaluation:
┌──────────────────────────────────────┐
│ Demand                   : 91 / 100  │
│ Trend Velocity           : 88 / 100  │
│ Competition Level        : 41 / 100  │
│ Supplier Reliability     : 86 / 100  │
│ Margin Margin            : 77 / 100  │
│ Shipping Score           : 82 / 100  │
│ Return Risk Penalty      : 19 / 100  │
│ AI-Discovery Potential   : 94 / 100  │
├──────────────────────────────────────┤
│ COMPOSITE OPPORTUNITY    : 89 / 100  │  ==> [STATUS: SCALABLE / APPROVED]
└──────────────────────────────────────┘
```

---

## 3. Human-in-the-Loop Feedback Pipeline
1. **AI Discovery:** Ingests candidate SKUs from supplier feeds and social trend APIs.
2. **Scoring:** Automated batch scoring computes POS across the catalog.
3. **Threshold Gate:** SKUs with POS $\ge 85$ get automatically queued for merchant review or automated staging.
4. **Validation & Creative Launch:** System generates structured schema, rich descriptions, and syndicates to distribution channels.

---

## Related Notes
- [[AI-Commerce-OS-MOC]]
- [[Commerce-OS-Three-Engine-Architecture]]
- [[Supplier-Abstraction-And-Dynamic-Routing]]
- [[Machine-Readable-Product-Identity-And-Distribution]]
