# Task and ValueTask Infrastructure

### Purpose
Located within [Asynchronous Programming](..), this directory covers the underlying types, allocation behaviors, and scheduling mechanics of the Task Parallel Library (TPL). It details the execution mechanics of promises in .NET.

### Scope
Topics include `Task`, `Task<T>`, `ValueTask<T>`, `TaskCompletionSource<T>`, task combinators (`Task.WhenAll`, `Task.WhenAny`), and custom `TaskScheduler` implementations.

### Content Guidelines
Document allocation-free asynchronous patterns using `ValueTask`, task state transitions, cold versus hot tasks, and defensive task composition in high-throughput services.
