# Software Engineering Second Brain
# المستودع المعرفي لهندسة البرمجيات

> **System:** Scalable, Database-Like Software Engineering Knowledge Graph
> **Architecture:** 4-Tier Strict Hierarchical Taxonomy (`Domain > Category > Subcategory > Atomic Concept Record`)
> **Metadata Standard:** Kebab-case naming, strict YAML frontmatter metadata, bidirectional semantic cross-linking
> **Status:** Production / Active

---

## 1. System Vision & Knowledge Architecture

This repository is engineered as an **Atomic, Relational Knowledge Graph** for computer science and software engineering concepts. Rather than unstructured notes or arbitrary topic dumps, every entry is treated as a **database-like atomic concept record** with formal schema definitions, explicit prerequisites, deep architectural explanations, executable code demonstrations, and bidirectional semantic cross-references.

### Core Architectural Principles
1. **Strict 4-Tier Hierarchy:** Every record is deterministically placed within `Domain > Category > Subcategory > Record`.
2. **Atomic Concept Records:** Self-contained units of knowledge addressing one concept with maximum technical depth, runnable code, and comparative decision heuristics.
3. **Machine-Readable Metadata:** Standardized YAML frontmatter on every concept file enables programmatic indexing, static site generation, and graph visualization.
4. **Bidirectional Semantic Graph:** Every atomic record links upstream to its Domain Index and Master Index, as well as horizontally to prerequisite and related concepts.
5. **Zero-Pollution & Anti-Hallucination Policy:** Strict prohibition of arbitrary folders, stub placeholders, or unverified invented concepts. Directory nodes are provisioned only when housing verified knowledge records.

---

## 2. Standardized Taxonomy & Naming Conventions

### A. Strict Directory & File Naming
- **Format:** All directory names, subdirectories, and Markdown file names use lowercase **`kebab-case`** exclusively (e.g., `relational-databases/`, `temporary-tables-vs-table-variables.md`).
- **Forbidden:** No spaces, no uppercase characters in content paths, no arbitrary acronyms without clear subcategory context.
- **Index Files:** Domain and root indexes are titled `README.md` for native GitHub/GitLab repository rendering.

### B. Standardized YAML Frontmatter Metadata Schema
Every atomic concept record begins with a YAML frontmatter block adhering to the following schema:

```yaml
---
id: <domain>-<category-abbrev>-<subcategory>-<concept-name> # Unique kebab-case ID
title: "<Standardized Concept Title in English>"
aliases:
  - "<Alternate English Name>"
  - "<Original Arabic Title or Dialect Name>"
domain: <domain-name>                                       # Root technical domain
category: <category-name>                                   # Tier-2 category
subcategory: <subcategory-name>                             # Tier-3 subcategory
type: concept | concept-comparison | architectural-pattern  # Record classification
status: draft | in-review | published                       # Lifecycle state
tags:
  - <tag-1>
  - <tag-2>
prerequisites:                                              # Upstream dependencies
  - "<domain>/<category>/<subcategory>/<prerequisite-record>"
related:                                                    # Horizontal semantic connections
  - "<domain>/<category>/<subcategory>/<related-record>"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```

### C. Anatomy of an Atomic Concept Record
Each Markdown concept record is structured with a uniform anatomy:
1. **Metadata Header:** Standardized YAML Frontmatter + Breadcrumb Navigation.
2. **Dual-Language Concept Title & Preservation:** Preserves original Arabic and English technical terms.
3. **Definition & Scope (التعريف والنطاق):** Clear, unambiguous architectural definitions and boundaries.
4. **Deep Architectural Explanation (التحليل المعماري والأداء):** Engine internals, memory vs. disk page allocations, concurrency behaviors, and query optimizer mechanics.
5. **Practical Code Examples (أمثلة عملية برمجية):** Production-grade, executable code demonstrating real-world behavior and edge cases.
6. **Comparative Matrix & Heuristics (خلاصة المقارنة):** Summary comparison tables and concrete decision trees for engineering trade-offs.
7. **Prerequisites & Verification (المتطلبات المسبقة والتحقق):** Checklists for validating runtime behavior in production or lab environments.
8. **Semantic Relationships & Cross-Links (الروابط والشبكة الدلالية):** Bidirectional links connecting to parent indexes, prerequisites, and related records.

---

## 3. Master Taxonomy Blueprint (14 Technical Domains)

The knowledge graph architecture maps all software engineering knowledge into **14 canonical technical domains**. To prevent arbitrary folder proliferation, physical directories are created strictly upon the addition of verified records.

```
                           [Software Engineering Second Brain]
                                            |
   +--------------------+-------------------+--------------------+--------------------+
   |                    |                   |                    |                    |
[fundamentals]     [paradigms]            [oop]               [memory]        [data-structures]
   |                    |                   |                    |                    |
[algorithms]      [concurrency]          [async]            [databases]         [networking]
   |                    |                   |                    |
[operating-systems] [architecture]   [design-patterns]       [security]
```

### Canonical Domain Specifications:
| # | Domain Identifier | Primary Scope & Categories | Status |
| :-: | :--- | :--- | :-: |
| **01** | `fundamentals` | Information theory, discrete math, data representations, type systems, boolean logic | *Schema Defined* |
| **02** | `paradigms` | Functional programming, imperative, declarative, reactive, logic programming | *Schema Defined* |
| **03** | `oop` | Encapsulation, inheritance, polymorphism, abstraction, SOLID principles, composition | *Schema Defined* |
| **04** | `memory` | Stack vs Heap, garbage collection algorithms, pointer mechanics, virtual memory, cache lines | *Schema Defined* |
| **05** | `data-structures` | Linear structures, trees (AVL, Red-Black, B-Tree), graphs, heaps, hash tables, bloom filters | *Schema Defined* |
| **06** | `algorithms` | Sorting, searching, dynamic programming, greedy methods, graph traversal, Big-O analysis | *Schema Defined* |
| **07** | `concurrency` | Threads, mutexes, semaphores, race conditions, deadlocks, lock-free structures, memory models | *Schema Defined* |
| **08** | `async` | Event loops, promises, async/await, non-blocking I/O multiplexing (`epoll`/`kqueue`), reactive streams | *Schema Defined* |
| **09** | `databases` | Relational engines (T-SQL, PostgreSQL), NoSQL, storage engines, indexing, ACID transactions | **Active (Live)** |
| **10** | `networking` | OSI layers, TCP/IP, HTTP/1-2-3, WebSockets, DNS, TLS handshake, load balancing, sockets | *Schema Defined* |
| **11** | `operating-systems` | Kernel architecture, processes, IPC, thread scheduling, paging, virtual file systems | *Schema Defined* |
| **12** | `architecture` | Monoliths, microservices, event-driven, CQRS, domain-driven design (DDD), hexagonal | *Schema Defined* |
| **13** | `design-patterns` | Creational (Factory, Singleton), Structural (Adapter, Decorator), Behavioral (Observer, Strategy) | *Schema Defined* |
| **14** | `security` | Authentication (OAuth2, JWT), Authorization (RBAC, ABAC), Cryptography, OWASP Top 10 | *Schema Defined* |

---

## 4. Active Repository Inventory & Navigation

The active knowledge base currently indexes the following verified, production-grade records:

<!-- BEGIN MASTER INVENTORY -->

| Domain | Category | Subcategory | Concept Title / Record | Type | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`databases`](databases/README.md) | `relational-databases` | `t-sql` | [Temporary Tables vs Table Variables in T-SQL](databases/relational-databases/t-sql/temporary-tables-vs-table-variables.md) | `concept-comparison` | `published` |

<!-- END MASTER INVENTORY -->

---

## 5. Knowledge Governance & Quality Assurance

### Anti-Pollution Governance Policy
- **No Arbitrary Directories:** Never create folders without immediate backing concept records.
- **No Stub / Hallucinated Records:** Concept records must contain exhaustive, verified technical explanations and runnable code examples. Empty or single-sentence files are rejected.
- **Deduplication:** When introducing new topics, verify existing domains and cross-link via `related` metadata rather than duplicating explanations.
- **Integrity Validation:** All internal markdown links and YAML frontmatter fields must pass programmatic validation before landing in the branch.
