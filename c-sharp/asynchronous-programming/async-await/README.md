# Async and Await Keywords

### Purpose
Located within [Asynchronous Programming](..), this directory details the compiler transformation, execution lifecycle, and syntax mechanics of `async` and `await` in C#. It examines how the Roslyn compiler rewrites asynchronous methods into state machines.

### Scope
Topics include the compiler-generated `IAsyncStateMachine`, `SynchronizationContext`, `ConfigureAwait(false)`, and custom awaiter patterns (`GetAwaiter`).

### Content Guidelines
Document synchronization context capture, async void anti-patterns, context switching costs, and step-by-step state machine lowering details.
