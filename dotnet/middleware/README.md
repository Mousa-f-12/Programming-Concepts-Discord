# ASP.NET Core Middleware Pipeline

### Purpose
Part of the [.NET Platform & Ecosystem](..) domain, this directory focuses on the HTTP request and response processing pipeline, request delegates, and pipeline branch topologies. It governs how incoming requests flow through the application.

### Scope
Topics include request pipeline construction (`Use`, `Run`, `Map`), conventional versus factory-based middleware (`IMiddleware`), exception handling middleware, and request buffering.

### Content Guidelines
Document pipeline execution order significance, performance optimization of request inspection, short-circuiting patterns, and asynchronous context propagation across delegates.
