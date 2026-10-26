---
layout: project
title: Owl
permalink: /projects/owl/
eyebrow: Numerical computing · Open source
intro: A scientific computing and deep learning framework for OCaml, covering arrays, linear algebra, statistics, automatic differentiation and neural networks.
role: Core developer; project lead since 2020
period: 2017–present
---
## The problem
Scientific computing needs dependable building blocks: efficient numerical operators, a way to express and differentiate computations, and a path from model definition to execution. Owl brings these capabilities to the OCaml ecosystem.

## My contribution
- **Framework design:** co-designed a computation-graph abstraction that separates definition from execution, supporting lazy evaluation, optimisation and compilation.
- **Core implementation:** worked on automatic differentiation and linear algebra, and implemented C convolution operators with cache-aware optimisation and parameter tuning.
- **Memory and interoperability:** led graph-level memory reuse, ONNX export and validation with ONNX Runtime; led the Zoo deployment framework with JavaScript and MirageOS backends.
- **Maintenance:** project lead and release manager since 2020, working on code review, issue discussions, CI/CD, releases, contributor coordination and documentation.

## A measured result
Graph-level memory reuse reduced **Mask R-CNN CPU inference memory by 86.6%**, from approximately **6.5 GB to 0.87 GB**, compared with the same framework without graph optimisation. Runtime, including graph construction, was reduced by 24.2% in that experiment. These are CPU inference results for the reported configuration.

The work is described in [Parallel and Memory-Efficient Distributed Edge Learning in B5G IoT Networks](https://ieeexplore.ieee.org/abstract/document/9956889/).

## Making the framework usable
I led the official tutorial, developed examples across numerical and machine-learning methods, and co-authored two [books about Owl]({{ '/books/' | relative_url }}#architecture). The project received two grants from the OCaml Software Foundation supporting maintenance and open-access publication.

<div class="links"><a class="button" href="https://github.com/owlbarn/owl">Source on GitHub ↗</a><a href="https://ocaml.xyz/">Owl website</a><a href="https://ocaml.xyz/book/">Tutorial</a></div>
