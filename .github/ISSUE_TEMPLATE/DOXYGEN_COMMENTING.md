# Doxygen-Style Code Documentation Guide (C++ + Python)

A practical, “keep it simple” guide for documenting code with **Doxygen-style comments** so humans (and future you) can navigate an API quickly.

---

## Contents

- [Goals](#goals)
- [The Keep It Simple Rules](#the-keep-it-simple-rules)
- [Recommended Tag Set](#recommended-tag-set-minimal-but-effective)
- [Formatting Basics](#formatting-basics)
  - [Doxygen comment styles](#doxygen-comment-styles)
- [C++](#c)
  - [File Header](#c-file-header-optional-but-useful)
  - [Class Header Template](#c-class-header-template)
  - [Method / Function Header Template](#c-method--function-header-template)
  - [Template Function (`@tparam`)](#c-template-function-tparam)
  - [Ownership & Lifetime Notes](#c-ownership--lifetime-notes-highly-recommended)
  - [Example Blocks (`@code`)](#c-example-blocks-code)
- [Python](#python)
  - [General Approach](#python-general-approach)
  - [Class Template](#python-class-template)
  - [Function / Method Template](#python-function--method-template)
  - [Documenting “Returns None”](#python-documenting-returns-none)
  - [Documenting Attributes / Members](#python-documenting-attributes--members)
- [What should I document? (Checklist)](#what-should-i-document-checklist)
- [Good vs Bad Examples](#good-vs-bad-examples)
- [Suggested Naming Conventions](#suggested-naming-conventions-docs)
- [Optional: Doxygen Grouping](#optional-doxygen-grouping-for-bigger-apis)
- [Quick Templates (Copy/Paste)](#quick-templates-copypaste)
- [Final Sanity Check](#final-sanity-check-before-you-commit)

---

## Goals

Good documentation should answer, in this order:

1. **What is this?** (purpose, responsibilities)
2. **How do I use it?** (parameters, return values, examples)
3. **What can go wrong?** (errors, exceptions, edge cases)
4. **Anything special?** (performance, thread-safety, ownership, invariants)

---

## The Keep It Simple Rules

- **One summary line** first (imperative, present tense): “Parses…”, “Computes…”, “Stores…”
- **Document the public surface** thoroughly (public classes, public functions, public constants).
- **Don’t narrate the code.** Explain intent and constraints, not every line.
- **Be explicit about ownership & lifetime** in C++.
- **Be explicit about units** (ms vs s, meters vs mm).
- **State preconditions** (what must be true before calling).
- **State postconditions** (what is true after).
- **If you need more than ~10 lines**, consider: is the API too complex?

---

## Recommended Tag Set (Minimal but Effective)

Use these consistently:

- `@brief` — one-line summary (often optional if first line is the brief)
- `@param <name>` — parameter meaning + constraints
- `@return` — return meaning (if non-void / non-None)
- `@throws` / `@exception` — exceptions (C++ and Python)
- `@note` — important behaviour / gotchas
- `@warning` — dangerous behaviour / sharp edges
- `@pre` / `@post` — preconditions and postconditions
- `@invariant` — class invariants
- `@tparam` — template parameters (C++)
- `@see` — related APIs
- `@example` — example usage (or use `@code ... @endcode` blocks)
- `@thread_safety` — concurrency notes (custom tag, but very useful)
- `@performance` — complexity and hotspots (custom tag)

Custom tags are fine; just keep them consistent.

---

## Formatting Basics

### Doxygen comment styles

**C++ (recommended):**
- `///` for brief blocks
- `/** ... */` for longer blocks

**Python:**
- Put a Doxygen-style block in the docstring, typically triple quotes `""" ... """`
- Doxygen will parse many common tags inside docstrings when configured.

---

## C++

### C++ File Header (Optional but useful)

Use this when files are “public” or non-obvious.

```cpp
/**
 * @file camera_controller.hpp
 * @brief High-level camera controller and lifecycle management.
 *
 * This file defines the CameraController facade which coordinates
 * camera acquisition, configuration, and streaming.
 *
 * @note Keep headers focused; implementation details belong in .cpp.
 */
```

### C++ Class Header Template

```cpp
/**
 * @brief Short description of what this class represents.
 *
 * Longer description:
 * - Key responsibilities
 * - What it owns (resources, threads, file handles)
 * - What it does NOT do (boundaries)
 *
 * @note Usage patterns (e.g., create, configure, start, stop).
 * @warning Any sharp edges.
 *
 * @invariant Describe conditions that are always true after construction
 *            and between public calls.
 *
 * @thread_safety
 *  - Thread-safe: yes/no/partially
 *  - Which methods are safe concurrently?
 *  - What locking model is used?
 */
class ExampleService {
public:
    /// @brief Constructs the service in a stopped state.
    ExampleService();

    /// @brief Starts background processing.
    void start();

    /// @brief Stops background processing and releases resources.
    void stop();
};
```

### C++ Method / Function Header Template

```cpp
/**
 * @brief One-line summary of what the function does.
 *
 * More detail if needed:
 * - Rules/constraints
 * - Side effects
 * - State transitions
 *
 * @param input What this is, constraints (e.g., must be non-empty).
 * @param timeout_ms Timeout in milliseconds. Use 0 for "no wait".
 *
 * @return What the return value means.
 *
 * @throws std::runtime_error When the underlying connection fails.
 *
 * @pre Service must be started.
 * @post Internal cache is updated on success.
 *
 * @note Any gotchas or subtle behaviours.
 * @warning Any dangerous behaviours.
 *
 * @performance O(n) where n is the number of items in the buffer.
 */
Result doWork(const std::string& input, int timeout_ms);
```

### C++ Template Function (`@tparam`)

```cpp
/**
 * @brief Applies a function to each element and collects results.
 *
 * @tparam T Input element type.
 * @tparam F Callable type: R(T) or R(const T&).
 *
 * @param items Items to transform.
 * @param fn Transformation function.
 *
 * @return Vector of transformed results.
 */
template <typename T, typename F>
auto transformAll(const std::vector<T>& items, F fn) -> std::vector<decltype(fn(items[0]))>;
```

### C++ Ownership & Lifetime Notes (Highly Recommended)

When relevant, document:

- Who owns pointers / references?
- Does the function store references beyond the call?
- Are returned pointers borrowed or owned?

Example:

```cpp
/**
 * @brief Registers a listener for events.
 *
 * @param listener Non-owning pointer. Must outlive this service OR call
 *                 unregisterListener() before destruction.
 *
 * @warning Passing a pointer to a temporary object will cause use-after-free.
 */
void registerListener(EventListener* listener);
```

### C++ Example Blocks (`@code`)

```cpp
/**
 * @brief Opens a connection and performs a handshake.
 *
 * @code
 * Client c;
 * c.connect("10.0.0.5", 9000);
 * c.handshake();
 * @endcode
 */
```

---

## Python

### Python General Approach

In Python, you’ll usually put Doxygen tags inside docstrings:

- Class docstring: documents role + attributes
- Method/function docstring: documents parameters/returns/raises

### Python Class Template

```python
class ExampleService:
    """
    @brief Short description of what this class does.

    Longer description:
    - Key responsibilities
    - What it manages (files, threads, sockets)
    - What it does NOT do (boundaries)

    @note Usage patterns and lifecycle.
    @warning Any sharp edges.

    @thread_safety
      - Thread-safe: yes/no/partially
      - Concurrency model (locks, asyncio, etc.)

    @invariant Conditions that remain true between public calls.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        @brief Creates the service in a disconnected state.

        @param host Remote host name or IP address.
        @param port Remote port number (1-65535).

        @raises ValueError If port is out of range.
        """
        self._host = host
        self._port = port
```

### Python Function / Method Template

```python
def do_work(input_text: str, timeout_s: float) -> str:
    """
    @brief One-line summary of what the function does.

    More detail if needed:
    - Rules/constraints
    - Side effects
    - State transitions

    @param input_text Input text to process. Must be non-empty.
    @param timeout_s Timeout in seconds. Use 0 for "no wait".

    @return Processed output text.

    @raises TimeoutError If the operation exceeds timeout_s.
    @raises ValueError If input_text is empty.

    @pre The service must be started.
    @post Internal cache is updated on success.

    @note Any gotchas.
    @performance O(n) where n is len(input_text).
    """
    ...
```

### Python Documenting “Returns None”

If it returns `None`, you can omit `@return` or be explicit:

```python
def stop() -> None:
    """
    @brief Stops processing and releases resources.

    @return None.
    """
```

### Python Documenting Attributes / Members

#### C++

Prefer documenting public members minimally; better to keep members private.
If you must document members:

```cpp
class Config {
public:
    /// @brief Timeout in milliseconds for network operations.
    int timeout_ms = 1000;
};
```

#### Python

Document in class docstring (and/or inline comments for internal use):

```python
class Config:
    """
    @brief Configuration options.

    Attributes:
      timeout_s: Timeout in seconds for network operations.
      retries: Number of retry attempts before failing.
    """
    timeout_s: float
    retries: int
```

---

## What should I document? (Checklist)

Document **every** public API with at least:

- Summary (`@brief` / first line)
- Parameters (`@param`)
- Returns (`@return`) if applicable
- Errors (`@throws` / `@raises`) if applicable
- Any essential notes (units, threading, ownership, side effects)

Also document:

- Any non-obvious performance characteristics
- Any non-obvious behaviour (caching, retries, backoff)
- Any state machine / lifecycle restrictions (start/stop, connect/disconnect)

---

## Good vs Bad Examples

### Bad (says nothing useful)

```cpp
/// @brief Does the thing.
void run();
```

### Better (intent + constraints)

```cpp
/**
 * @brief Starts the worker loop and begins processing queued jobs.
 *
 * @pre enqueueJob() may be called before run(), but jobs will not execute until run().
 * @post isRunning() returns true on success.
 *
 * @thread_safety Not thread-safe. Call from a single control thread.
 */
void run();
```

---

## Suggested Naming Conventions (Docs)

- Use consistent units suffixes in names:
  - `timeout_ms`, `period_s`, `distance_m`, `angle_rad`
- If a value is optional, say so explicitly:
  - “If None, uses default X”
  - “If empty, disables Y”

---

## Optional: Doxygen Grouping (For Bigger APIs)

If you have modules, group them:

```cpp
/**
 * @defgroup Telemetry Telemetry
 * @brief Telemetry collection and export.
 */
///@{
/** @brief Sends a telemetry sample. */
void sendSample(...);
///@}
```

---

## Quick Templates (Copy/Paste)

### C++ function (short)

```cpp
/// @brief <one line summary>
/// @param a <meaning>
/// @param b <meaning>
/// @return <meaning>
/// @throws <exception> <when>
```

### C++ function (long)

```cpp
/**
 * @brief <one line summary>
 *
 * <details>
 *
 * @param a <meaning + constraints>
 * @param b <meaning + constraints>
 * @return <meaning>
 * @throws <exception> <when>
 * @pre <precondition>
 * @post <postcondition>
 * @note <note>
 * @warning <warning>
 */
```

### Python function (docstring)

```python
def f(...):
    """
    @brief <one line summary>

    @param x <meaning + constraints>
    @return <meaning>
    @raises <Exception> <when>
    @note <note>
    """
```

---

## Final Sanity Check (before you commit)

- Can someone new to the code use the API from just the docs?
- Are units and constraints stated?
- Are errors/edge cases documented?
- Does the summary match what the code actually does?
- Is the doc short enough to stay maintained?
