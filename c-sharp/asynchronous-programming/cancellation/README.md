# Cooperative Cancellation

### Purpose
Located within [Asynchronous Programming](..), this directory focuses on reliable, thread-safe cancellation workflows in asynchronous and long-running C# operations. It covers clean termination of workloads without resource leaks or thread aborts.

### Scope
Topics include `CancellationToken`, `CancellationTokenSource`, linked cancellation tokens, timeout registration, token polling versus throw mechanics, and `OperationCanceledException` handling.

### Content Guidelines
Store cancellation propagation patterns through asynchronous call stacks, resource cleanup guarantees during cancellation, and timeout resilience strategies.
