# Database Design

## Purpose

This document describes the logical database design for the Marketplace Intelligence Platform.

The database is designed to support:

- Operational reporting
- Business analytics
- Machine learning feature generation
- REST API queries
- Dashboard visualizations

---

# Core Entities

1. Customers
2. Orders
3. Order Items
4. Products
5. Sellers
6. Payments
7. Reviews
8. Geolocation
9. Product Categories

---

# Primary Relationships

Customer
│
└── places ───► Orders

Orders
│
├── contains ───► Order Items
├── has ───────► Payments
├── receives ─► Reviews

Order Items
│
├── references ─► Products
└── sold by ───► Sellers

Customers
│
└── located in ─► Geolocation

Sellers
│
└── located in ─► Geolocation

Products
│
└── belongs to ─► Product Category