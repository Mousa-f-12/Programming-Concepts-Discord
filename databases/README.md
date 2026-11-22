# Databases Knowledge Domain Index
# فهرس مجال قواعد البيانات

> **Domain ID:** `databases`  
> **Master Index:** [Software Engineering Second Brain Catalog](../README.md)  
> **Status:** Active (Production)  
> **Taxonomy Level:** Domain (Level 1)

---

## 1. Domain Scope & Architecture — نطاق المجال والمعمارية
The **Databases** domain encompasses physical and logical data storage systems, query compilation and optimization engines, indexing strategies, transaction semantics (ACID/BASE), distributed consensus, and relational/non-relational database engines.

Knowledge records in this domain are categorized strictly under the 4-tier taxonomy:  
`Domain (databases) > Category > Subcategory > Atomic Concept Record`

```
databases/
├── README.md (This Domain Index)
└── relational-databases/                     # Category
    └── t-sql/                                # Subcategory
        └── temporary-tables-vs-table-variables.md  # Atomic Concept Record
```

---

## 2. Taxonomy & Active Knowledge Records — الفهرس الهيكلي والسجلات المفعلة

<!-- BEGIN DOMAIN INVENTORY -->

### Category: `relational-databases`

#### Subcategory: `t-sql`

| Concept ID | Title / Record | Type | Status |
| :--- | :--- | :--- | :--- |
| `db-rel-tsql-temp-tables-vs-table-variables` | [Temporary Tables vs Table Variables in T-SQL](relational-databases/t-sql/temporary-tables-vs-table-variables.md) | `concept-comparison` | `published` |

<!-- END DOMAIN INVENTORY -->

---

## 3. Concept Summary: Temporary Tables vs Table Variables
- **Summary:** Comprehensive architectural and practical comparison between Temporary Tables (`#Temp`, `##Temp`) and Table Variables (`@Table`) in T-SQL.
- **Key Takeaways:**
  - Both persist to `tempdb` memory/disk buffers; table variables are not purely in-memory.
  - Temporary Tables support statistical histograms and post-creation indexes, preventing bad cardinality estimates.
  - Table Variables do not participate in explicit user transaction rollbacks (`ROLLBACK TRANSACTION` does not revert changes).
  - Temporary Tables are visible to child execution scopes and dynamic SQL; Table Variables are strictly batch/proc scoped.
- **Full Atomic Record:** [Read Full Deep-Dive Record](relational-databases/t-sql/temporary-tables-vs-table-variables.md)

---

## 4. Cross-Domain Interconnections — الروابط البينية بين المجالات

Knowledge records in the `databases` domain interconnect with adjacent technical domains across the Second Brain:

```
                      +-----------------------------+
                      |   [Master Second Brain]     |
                      |        (../README.md)       |
                      +--------------+--------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+------------------------+                       +------------------------+
|      [concurrency]     |                       |   [operating-systems]  |
|  - Transaction Locks   | <-------------------> |  - Buffer Cache & I/O  |
|  - Isolation Levels    |     [databases]       |  - Page Flush Mechanics|
+------------------------+                       +------------------------+
             ^                                               ^
             |                                               |
             +-----------------------+-----------------------+
                                     |
                                     v
                         +-----------------------+
                         |        [memory]       |
                         |  - Buffer Pool Alloc  |
                         |  - Contention (PFS)   |
                         +-----------------------+
```

1. **`concurrency`**: Relational locking, latch contention, latch-free memory tables, and snapshot isolation.
2. **`operating-systems`**: Direct I/O vs buffered I/O, sector alignment, log write flushing (`WAL`), and write amplification.
3. **`memory`**: Page buffer pools, execution grant memory, spill-to-disk thresholds.
4. **`data-structures`**: B-Tree and B+ Tree index structures, Hash buckets, Columnar inverted indexes.

---

## 5. Domain Governance & Contribution Standard
To add a new database concept record:
1. Identify the exact category (e.g., `relational-databases`, `distributed-storage`, `key-value-stores`).
2. Identify or establish the subcategory (e.g., `t-sql`, `postgres-internals`, `acid-semantics`).
3. Name the record using strict `kebab-case.md`.
4. Populate all standardized YAML frontmatter fields (`id`, `title`, `domain`, `category`, `subcategory`, `type`, `status`, `tags`, `prerequisites`, `related`).
5. Ensure the record contains: Definition, Deep Architectural Explanation, Runnable Code Examples, Comparative Matrix, and Bidirectional Links.
6. Register the record in this index (`databases/README.md`) and the master catalog (`../README.md`).
