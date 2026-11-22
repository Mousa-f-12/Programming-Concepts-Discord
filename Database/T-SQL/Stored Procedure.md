# 📘 Stored Procedure — Summary

## 1. Definition

A **Stored Procedure** is a collection of `T-SQL` statements and instructions stored inside the database under a specific name. It can be called and executed whenever needed.

---

## 2. Why Do We Use Stored Procedures?

| Reason | Description |
|---|---|
| ⚡ **Performance** | إمكانية إعادة استخدام خطط التنفيذ وتحسين تنظيم تنفيذ الاستعلامات. |
| 🔐 **Security** | التحكم بصلاحيات الوصول إلى البيانات من خلال السماح بتنفيذ إجراءات محددة. |
| 🛠️ **Maintainability** | تجميع منطق العمليات في مكان مركزي لتسهيل تعديله وصيانته. |
| ♻️ **Reusability** | إعادة استخدام نفس الإجراء من تطبيقات أو أجزاء مختلفة. |

---

## 3. What Can a Stored Procedure Contain?

تستطيع `Stored Procedure` احتواء مجموعة واسعة من تعليمات ومفاهيم `T-SQL`:

| Concept | Usage |
|---|---|
| `SELECT` | قراءة البيانات. |
| `INSERT` | إضافة البيانات. |
| `UPDATE` | تعديل البيانات. |
| `DELETE` | حذف البيانات. |
| `DECLARE` | تعريف المتغيرات المحلية. |
| `SET` | إسناد القيم للمتغيرات. |
| `IF / ELSE` | تنفيذ الأوامر حسب الشروط. |
| `WHILE` | تكرار تنفيذ الأوامر. |
| `BEGIN / END` | تجميع الأوامر داخل بلوك. |
| `TRY / CATCH` | معالجة الأخطاء. |
| `TRANSACTION` | ضمان تنفيذ مجموعة عمليات كوحدة واحدة. |
| `EXEC` | استدعاء إجراءات أخرى أو تنفيذ SQL ديناميكي. |
| `OUTPUT` | إرجاع قيم عبر Parameters. |
| `RETURN` | إرجاع قيمة عددية من الإجراء. |
| `THROW` | إطلاق أخطاء مخصصة. |
| `CTE` | تنظيم الاستعلامات المعقدة. |
| `Temporary Tables` | تخزين نتائج مؤقتة. |
| `Table Variables` | تخزين مجموعات بيانات مؤقتة. |
| `TVP` | تمرير جدول كامل كـ Parameter. |
| `Cursor` | معالجة السجلات واحداً تلو الآخر. |
| `Dynamic SQL` | بناء استعلامات وتنفيذها أثناء التشغيل. |
| `DDL` | إنشاء وتعديل وحذف كائنات قاعدة البيانات. |

---

## 4. Stored Procedure Lifecycle

| Command | Description |
|---|---|
| `CREATE PROCEDURE` | إنشاء إجراء جديد. |
| `ALTER PROCEDURE` | تعديل إجراء موجود. |
| `DROP PROCEDURE` | حذف إجراء موجود. |
| `EXEC` | تنفيذ الإجراء. |

---

## 5. Important Engineering Notes

- **Performance:** لا تعني `Stored Procedure` بالضرورة أداءً أفضل دائماً.
- **Set-Based Operations:** يُفضّل استخدام العمليات المعتمدة على المجموعات بدلاً من `Cursor` متى أمكن.
- **SQL Injection:** يجب الحذر من `SQL Injection` عند استخدام `Dynamic SQL`.
- **Data Integrity:** يُفضّل الجمع بين `TRY...CATCH` و`TRANSACTION` عند تنفيذ العمليات المترابطة التي تتطلب سلامة البيانات.

---

## 6. Summary

تعامل مع `Stored Procedure` باعتبارها وحدة برمجية محفوظة داخل `SQL Server`، تستطيع:

- تنفيذ استعلامات وعمليات منطقية متكاملة.
- استقبال `Parameters` وإرجاع نتائج.
- التعامل مع الأخطاء والمعاملات.
- تنظيم منطق العمليات وإعادة استخدامه.

> **Core Concept:** `Stored Procedure` ليست مجرد استعلام محفوظ، بل وحدة تنفيذ برمجية داخل قاعدة البيانات يمكنها الجمع بين الاستعلامات والتحكم بالتدفق ومعالجة الأخطاء وإدارة المعاملات.
