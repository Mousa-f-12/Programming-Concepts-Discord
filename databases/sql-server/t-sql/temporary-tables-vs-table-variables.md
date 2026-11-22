---
id: db-rel-tsql-temp-tables-vs-table-variables
title: "Temporary Tables vs Table Variables in T-SQL"
aliases:
  - "Differences between Temp Table vs Variable Table"
  - "Temp Tables vs Table Variables"
  - "الفرق بين الجداول المؤقتة ومتغيرات الجداول في T-SQL"
domain: databases
category: relational-databases
subcategory: t-sql
type: concept-comparison
status: published
tags:
  - databases
  - sql-server
  - t-sql
  - tempdb
  - storage-engine
  - query-optimization
prerequisites:
  - "databases/relational-databases/t-sql/t-sql-fundamentals"
  - "databases/relational-databases/sql-server/tempdb-architecture"
related:
  - "databases/relational-databases/sql-server/transaction-log-mechanics"
  - "databases/relational-databases/sql-server/cardinality-estimation-and-statistics"
created: "2026-11-22"
updated: "2026-11-22"
---

# الفرق بين Temporary Tables و Table Variables في T-SQL
# Temporary Tables vs Table Variables in T-SQL

> **Concept ID:** `db-rel-tsql-temp-tables-vs-table-variables`  
> **Domain:** [databases](../../README.md) > `relational-databases` > `t-sql`  
> **Central Index:** [Second Brain Master Index](../../../README.md)

---

## 1. Definition and Scope — التعريف والنطاق

### النطاق والتعريف بالعربية (Preserved Original Definition)
* **Temporary Tables (`#`):** جداول مؤقتة تُنشأ باستخدام `CREATE TABLE`، وتُخزّن في قاعدة البيانات `tempdb`. يمكن أن تكون محلية (`#Temp`) أو عامة (`##Temp`).
* **Table Variables (`@`):** متغيرات تأخذ شكل جدول، ونُنشئها باستخدام `DECLARE`، وتُستخدم لتخزين مجموعة من الصفوف مؤقتاً.

### Architectural Definition & Scope
In Microsoft SQL Server and Transact-SQL (T-SQL), both **Temporary Tables** and **Table Variables** serve as temporary relational storage structures instantiated in `tempdb`. However, their architectural allocation, operational scopes, and lifecycle semantics differ significantly:

1. **Temporary Tables (`#Local` / `##Global`):**
   - **Local Temporary Tables (`#Temp`):** Prefixed with a single hash (`#`). Scoped strictly to the creating user session and execution level. Visible to child procedures invoked from the calling scope, and automatically dropped when the creating connection closes or when explicitly destroyed via `DROP TABLE`.
   - **Global Temporary Tables (`##Temp`):** Prefixed with a double hash (`##`). Accessible across all concurrent database sessions. Dropped automatically only when the creating session disconnects and all active queries referencing the table terminate.
2. **Table Variables (`@Table`):**
   - Declared with a leading `@` symbol using syntax analogous to a standard variable (`DECLARE @Name TABLE (...)`).
   - Scoped strictly to the immediate batch, stored procedure, or user-defined function (UDF) in which they are declared. Out-of-scope for child batches or dynamic SQL executions (`sp_executesql`).

---

## 2. Lifetime — دورة الحياة

### دورة الحياة بالعربية (Preserved Original Definition)
* **Temporary Tables:** تبقى موجودة حتى نحذفها يدوياً أو ينتهي الاتصال (Session) الذي أنشأها.
* **Table Variables:** تنتهي تلقائياً عند انتهاء النطاق الذي أُنشئت داخله، مثل Batch أو Stored Procedure.

### Lifecycle & Scope Boundaries
| Characteristic | Temporary Table (`#Temp`) | Table Variable (`@Table`) |
| :--- | :--- | :--- |
| **Instantiation** | `CREATE TABLE #Temp (...)` or `SELECT ... INTO #Temp` | `DECLARE @Table TABLE (...)` |
| **Boundary Scope** | Session & Child execution scopes | Current Batch, Stored Procedure, or Function only |
| **Cross-Procedure Scope** | Accessible in downstream child stored procedures | Inaccessible to child stored procedures or dynamic SQL |
| **Destruction** | Manual (`DROP TABLE #Temp`) or Session disconnect | Automatic at batch termination |
| **User-Defined Functions** | **Prohibited** inside UDFs | **Allowed** inside Multi-Statement Table-Valued Functions (MSTVFs) |

---

## 3. Performance and Usage — الأداء والاستخدام

### الأداء والاستخدام بالعربية (Preserved Original Definition)
* **Temporary Tables:** مناسبة للبيانات الكبيرة والعمليات المعقدة، وتدعم الفهارس والإحصائيات (Statistics) بشكل أفضل.
* **Table Variables:** مناسبة للبيانات الصغيرة والعمليات البسيطة، لكن إمكانيات تحسين الاستعلامات فيها محدودة مقارنة بالجداول المؤقتة.

### Deep Architectural Explanation: Engine Internals

#### A. Physical Storage Mechanism (`tempdb`)
A common misconception is that Table Variables live purely in memory while Temporary Tables reside on disk. **Both physical structures reside in `tempdb`**. 
- SQL Server allocates pages (PFS/GAM/SGAM/IAM) in the `tempdb` buffer pool for both.
- If data volume exceeds available memory buffer allocations, pages for **both** types spill to the `tempdb` data files on physical storage.

#### B. Query Optimizer Statistics & Cardinality Estimation
- **Temporary Tables:** 
  - The Query Optimizer creates and dynamically maintains full column-level distribution statistics (distribution histograms) for `#Temp` tables.
  - Generates accurate cardinality estimations during compilation, allowing the engine to pick optimal join strategies (e.g., Hash Match vs Nested Loops).
- **Table Variables:** 
  - Table Variables do **not** maintain distribution statistics.
  - Prior to SQL Server 2019, the cardinality estimator always assumed a fixed cardinality of **1 row** (or 100 rows in specific table-valued parameters), regardless of whether 1 row or 5,000,000 rows were inserted. This frequently results in catastrophic execution plans (such as choosing an inefficient nested-loop index seek against millions of rows).
  - *SQL Server 2019+ Enhancement:* Adaptive Query Processing introduced **Table Variable Deferred Compilation**, which delays compilation of statements referencing table variables until the first execution to use actual row counts, partially mitigating this limitation.

#### C. Indexing Capabilities
- **Temporary Tables:** Support explicit index creation after table creation (`CREATE NONCLUSTERED INDEX idx_col ON #Temp(col)`), clustered indexes, filtered indexes, and columnstore indexes.
- **Table Variables:** Historically only supported indexes implicitly via `PRIMARY KEY` and `UNIQUE` constraints defined at declaration time. SQL Server 2014 added inline index definition syntax (`INDEX idx_col (col)`), but non-inline post-declaration `CREATE INDEX` remains unsupported.

#### D. Recompilations
- **Temporary Tables:** Modifications and data volume shifts past recompile thresholds trigger statement-level recompilations.
- **Table Variables:** Because they lack statistics, they rarely trigger query plan recompilations, reducing CPU recompile overhead at the expense of potentially suboptimal plans.

---

## 4. Transaction Logs — سجلات المعاملات

### سجلات المعاملات بالعربية (Preserved Original Definition)
* **Temporary Tables:** عمليات التعديل عليها تُسجّل في سجل المعاملات، ويمكن التراجع عنها باستخدام `ROLLBACK`.
* **Table Variables:** التعديلات عليها لا تُلغى عند تنفيذ `ROLLBACK`؛ وهذه نقطة مهمة جداً عند التعامل مع المعاملات.

### Transactional Mechanics & ACID Properties
The behavioral difference during transaction rollbacks is one of the most critical functional distinctions in T-SQL:

- **Temporary Tables participate in user transaction rollbacks:** Modifications (INSERT, UPDATE, DELETE) executed within a user transaction block (`BEGIN TRANSACTION ... ROLLBACK TRANSACTION`) are fully rolled back.
- **Table Variables do NOT participate in user transaction rollbacks:** Like scalar variables (`@Counter = @Counter + 1`), mutations made to a Table Variable are committed instantly to its internal state. A subsequent `ROLLBACK TRANSACTION` has **no effect** on the rows inside `@Table`.

---

## 5. Practical Code Examples — أمثلة عملية

### Example 1: Creation, Scope, and Indexing
```sql
-- ========================================================
-- 1. Temporary Table (#Temp) with Explicit Indexing
-- ========================================================
CREATE TABLE #TempOrders (
    OrderID INT NOT NULL PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL
);

-- Explicitly create non-clustered index after creation
CREATE NONCLUSTERED INDEX IX_TempOrders_CustomerID 
ON #TempOrders (CustomerID);

INSERT INTO #TempOrders (OrderID, CustomerID, OrderAmount)
VALUES (101, 1001, 250.00), (102, 1002, 1500.50);

SELECT * FROM #TempOrders WHERE CustomerID = 1001;

-- Clean up
DROP TABLE #TempOrders;


-- ========================================================
-- 2. Table Variable (@Table) with Inline Indexing (SQL 2014+)
-- ========================================================
DECLARE @VarOrders TABLE (
    OrderID INT NOT NULL PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL,
    INDEX IX_VarOrders_CustomerID (CustomerID) -- Inline index definition
);

INSERT INTO @VarOrders (OrderID, CustomerID, OrderAmount)
VALUES (201, 2001, 400.00), (202, 2002, 850.75);

SELECT * FROM @VarOrders WHERE CustomerID = 2001;
-- Automatically deallocated at the end of the batch
```

---

### Example 2: Transaction Rollback Proof (إثبات التراجع المعاملاتي)
This test demonstrates the fundamental transactional divergence:
```sql
-- Setup test containers
CREATE TABLE #TempRollbackTest (ID INT);
DECLARE @VarRollbackTest TABLE (ID INT);

BEGIN TRANSACTION;

    INSERT INTO #TempRollbackTest (ID) VALUES (1);
    INSERT INTO @VarRollbackTest (ID) VALUES (1);

-- Rollback the transaction
ROLLBACK TRANSACTION;

-- Query Results:
-- 1. Temporary table is empty: changes were successfully reverted
SELECT 'Temporary Table Count' AS Target, COUNT(*) AS Row_Count 
FROM #TempRollbackTest; 
-- Result: 0 rows

-- 2. Table variable retains data: changes were NOT reverted!
SELECT 'Table Variable Count' AS Target, COUNT(*) AS Row_Count 
FROM @VarRollbackTest; 
-- Result: 1 row

-- Clean up
DROP TABLE #TempRollbackTest;
```

---

### Example 3: Stored Procedure & Dynamic SQL Scope
```sql
-- Demonstrating that #Temp is accessible in child dynamic SQL,
-- while @Var is strictly inaccessible.
CREATE TABLE #SessionTemp (Val VARCHAR(50));
INSERT INTO #SessionTemp VALUES ('Accessible in Dynamic SQL');

DECLARE @BatchVar TABLE (Val VARCHAR(50));
INSERT INTO @BatchVar VALUES ('Inaccessible in Dynamic SQL');

-- Dynamic SQL child scope execution:
EXEC sp_executesql N'SELECT * FROM #SessionTemp;'; 
-- SUCCESS: Returns data

-- The following would fail with an error because @BatchVar is out-of-scope:
-- EXEC sp_executesql N'SELECT * FROM @BatchVar;'; 
-- ERROR: Must declare the table variable "@BatchVar".

DROP TABLE #SessionTemp;
```

---

## 6. Use Cases — حالات الاستخدام

### حالات الاستخدام بالعربية (Preserved Original Definition)
* **Temporary Tables:** استخدمها عندما تتعامل مع بيانات كثيرة أو عمليات معقدة أو تحتاج إلى التراجع عن التعديلات.
* **Table Variables:** استخدمها عندما تحتاج إلى تخزين عدد صغير من الصفوف مؤقتاً لتنفيذ عملية بسيطة.

### Technical Decision Heuristics
Use the following architectural guidelines to choose between them:

```
                                [Data Volume & Complexity]
                                            |
             -----------------------------------------------------------------
            |                                                                 |
     [Small Volume (<100 rows)]                                    [Large Volume (>1000 rows)]
     [No complex joins/filters]                                    [Complex joins / aggregations]
     [Inside User-Defined Functions]                               [Requires explicit indexing / DDL]
     [Need logging across rollback]                                [Requires transactional rollback]
            |                                                                 |
            v                                                                 v
    Use: Table Variable (@)                                       Use: Temporary Table (#)
```

1. **Choose Temporary Tables (`#Temp`) when:**
   - The result set contains moderate to large volumes of data (> 1,000 rows).
   - The dataset participates in complex joins, aggregations, or filters where index histograms and accurate cardinality estimation are vital.
   - You need explicit composite or non-clustered indexes created dynamically.
   - You require modifications to be revoked if the surrounding transaction rolls back.
   - You are altering schema dynamically (`ALTER TABLE`).

2. **Choose Table Variables (`@Table`) when:**
   - The dataset is trivial (cardinality under 100 rows, e.g., lookup lists, IDs passed as parameters).
   - Working inside scalar or multi-statement table-valued user-defined functions (UDFs) where `#Temp` is syntactically illegal.
   - You specifically want to log errors or audit metadata inside a transaction block and preserve those rows even when an operational error causes a `ROLLBACK`.
   - You wish to minimize recompile events on fast, high-throughput stored procedures.

---

## 7. Comparative Summary — خلاصة المقارنة

### جدول المقارنة الشامل (Preserved Original Table & Expanded Architectural Matrix)

| معيار المقارنة / Feature | Temporary Table (`#Temp`) | Table Variable (`@Table`) |
| :--- | :--- | :--- |
| **طريقة الإنشاء / Creation** | `CREATE TABLE #Temp` / `SELECT INTO` | `DECLARE @Table TABLE` |
| **صيغة الاسم / Identifier** | `#Temp` (محلي) / `##Temp` (عام) | `@Temp` |
| **موقع التخزين / Storage Engine** | قاعدة البيانات `tempdb` (Memory buffer + Disk) | تستخدم موارد SQL Server ومخزنة في `tempdb` |
| **نطاق دورة الحياة / Lifetime** | اتصال الجلسة أو الحذف اليدوي (`DROP TABLE`) | نطاق الـ Batch أو Stored Procedure فقط |
| **دعم الإحصائيات / Statistics** | تدعمها وتنشئ Distribution Histograms | محدودة / غير مدعومة (تقدير 1 صف قبل SQL 2019) |
| **التأثر بالتراجع / ROLLBACK** | يُلغي التعديلات (Fully transactional) | لا يُلغي التعديلات (State preserved) |
| **الفهارس الإضافية / Explicit Indexes** | تدعم `CREATE INDEX` بعد الإنشاء | فهارس ضمنية فقط عند التعريف (Inline Index) |
| **الدوال المعرفة / UDF Support** | غير مسموحة داخل User-Defined Functions | مسموحة وتستخدم في Multi-Statement TVFs |
| **حدود الـ Dynamic SQL** | مرئية داخل الاستدعاءات الفرعية لـ `sp_executesql` | غير مرئية وغير قابلة للوصول داخل Dynamic SQL |
| **إعادة الترجمة / Recompilation** | قد تسبب Recompilation عند تغير البيانات | نادراً ما تسبب Recompilation |
| **تعديل الهيكل / DDL Alteration** | تدعم `ALTER TABLE` | لا تدعم `ALTER TABLE` بعد التصريح |

### ملاحظة هندسية (Preserved Original Engineering Note)
> **ملاحظة هندسية:** لا تفترض أن Table Variable أسرع دائماً لأنها صغيرة أو أن Temporary Table أبطأ بسبب التسجيل. الأداء يعتمد على حجم البيانات، وطبيعة الاستعلام، وإصدار SQL Server.

**Engineering Insight:** Never assume a Table Variable is faster simply because it is called a "variable", nor that a Temporary Table is slower due to logging overhead. Both write to `tempdb` transaction logs (though table variables exhibit slightly reduced logging overhead due to their non-rollback nature). For queries involving medium or large datasets, the absence of distribution statistics in Table Variables can lead the query optimizer to make disastrous plan choices that are orders of magnitude slower than a Temporary Table.

---

## 8. Prerequisites & Verification — المتطلبات المسبقة والتحقق

### Prerequisites
Before implementing temporary storage structures in production T-SQL:
- Familiarity with basic SQL Server transaction syntax (`BEGIN TRAN`, `COMMIT TRAN`, `ROLLBACK TRAN`).
- Understanding of SQL Server `tempdb` architecture and page allocation.
- Understanding of Execution Plans and Cardinality Estimation.

### Verification Checklist in SSMS / Azure Data Studio
1. **Execution Plan Inspection:** Check the "Estimated Number of Rows" vs "Actual Number of Rows" in SSMS execution plans when querying `@Table` vs `#Temp`.
2. **Tempdb Usage Verification:** Execute `SELECT * FROM sys.tables WHERE name LIKE '%#%'` to inspect active session tables in `tempdb`.
3. **Rollback Behavior:** Validate that operational error handlers (`TRY...CATCH`) account for the persistence of `@Table` mutations during transactions.

---

## 9. Semantic Relationships & Cross-Links — الروابط والشبكة الدلالية

### Upstream Prerequisites
- [Central Second Brain Catalog](../../../README.md)
- [Databases Domain Index](../../README.md)

### Related Database Architecture Topics
- *`databases/relational-databases/sql-server/tempdb-allocation-and-contention`* (Planned)
- *`databases/relational-databases/sql-server/query-optimizer-and-statistics`* (Planned)
- *`databases/relational-databases/sql-server/transaction-log-internals`* (Planned)
