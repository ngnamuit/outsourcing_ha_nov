# Inventory Advanced

### Overview
The **Inventory Advanced** module enhances Odoo Inventory by introducing advanced configuration for **racking systems** and **pallet management**.

It adds configurable parameters such as **beam width**, **pallet type**, and **capacity**, enabling more precise control and optimization of pallet storage within warehouse racks.

---

### Background
In standard Odoo, warehouse racks can be described using simple parameters like beam width, pallet capacity, and pallet type.  
For example:

| Rack Code | Beam Width (mm) | Capacity (Pallets) | Pallet Type       |
|------------|-----------------|--------------------|-------------------|
| RACK-2440-3P | 2440 | 3 | 600 mm (narrow) |
| RACK-2400-2P | 2400 | 2 | 1100 mm (wide) |
| RACK-2740-4P | 2740 | 4 | 600 mm (narrow) |
| RACK-2740-3P | 2740 | 3 | 800 mm (standard) |

However, **Odoo does not optimize pallet placement on each beam**.  
For instance:
- On a 2440 mm beam, you could fit *two 600 mm pallets and one 1000 mm pallet*.
- On a 2740 mm beam, you could fit *four 600 mm pallets* — maximizing space without exceeding the beam load limit.

Although **weight is rarely a constraint** (each beam can hold up to 1500 kg, while most pallets weigh under 300 kg), space optimization is critical for efficient warehouse utilization.

---

### Example: Location Structure
Warehouse locations can follow a structured code system such as:

```
AC.L3.4
```

Where:
- **AC** = Row  
- **L3** = Level 3  
- **4** = Column 4  
- **a/b/c** = Sub-positions on the same beam

If multiple pallets are stored on the same beam, sub-positions can be used:
```
AC.L3.4-a
AC.L3.4-b
AC.L3.4-c
```

---

### Example Beam Specification

| Code | Height (mm) | Width (mm) | Depth (mm) | Capacity (kg) |
|------|--------------|-------------|-------------|----------------|
| AC.L1.4 | 1200 | 2440 | 1200 | 1500 |
| AC.L2.4 | 1200 | 2440 | 1200 | 1500 |
| AC.L3.4 | 1200 | 2440 | 1200 | 1500 |
| AC.L4.4 | 1200 | 2440 | 1200 | 1500 |
| AF.L1.1 | 1200 | 2740 | 1200 | 1500 |
| AF.L2.1 | 1200 | 2740 | 1200 | 1500 |
| AF.L3.1 | 1200 | 2740 | 1200 | 1500 |
| AF.L4.1 | 1200 | 2740 | 1200 | 1500 |
| AF.L1.2 | 1200 | 2740 | 1200 | 1500 |

Most pallets weigh less than **300 kg**, while each beam can support up to **1500 kg**, so weight is rarely a limiting factor.  
The main challenge is **maximizing beam width utilization** per pallet combination.

---

### Business Question

Currently, this functionality is not available in the native Odoo ERP.  
It could potentially be implemented as a **custom Odoo add-on**, or may exist as part of a **dedicated WMS (Warehouse Management System)** extension.

> **Question:**  
> Can this pallet optimization logic be developed as a simple Odoo plugin,  
> or does an existing module already provide this capability?

---

### Objective
This module aims to extend Odoo’s stock management capabilities by introducing:

- A **Rack Configuration Model**  
  to define beam width, capacity, and pallet types.

- **Beam Optimization Logic**  
  to automatically suggest or validate pallet placement based on available beam width and pallet dimensions.

- **Custom Location Coding Rules**  
  supporting structures like `Row.Level.Column-Position`.

- **Integration Hooks**  
  for future extensions or connection to full-scale **Warehouse Management Systems (WMS)**.

---

### Reference Documentation
For detailed functional design and technical implementation notes, please refer to:  
📘 [Solution Page v2.0 (Notion)](https://www.notion.so/ngnamuit/Solution-page-v2-0-298037d477b7809796aac5ee18c05815)

---

### Access Control
Available to **Warehouse Managers** only.

---

### Dependencies
- **Odoo 18 Enterprise**
- **Inventory (`stock`)** module

---

### Author
Developed by **Nam Nguyen**  
_For: Advanced Warehouse & Pallet Optimization Initiative_
