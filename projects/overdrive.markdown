---
layout: project
title: OverDrive
permalink: /projects/overdrive/
eyebrow: Multimodal inference · Research
intro: Investigating how VLM/VLA driving models can deliver useful planning results within the time available in a changing scene.
role: Project lead, Karlsruhe Institute of Technology
period: 2023–2026
---
## The problem
A driving model's answer has a limited useful lifetime. OverDrive studies inference execution and scheduling in relation to those time constraints, with attention to what measurements can actually establish.

## My contribution
I designed and led the development of a common model-adaptation and replay-evaluation framework, using AI coding tools to help implement adapters for **four open-source driving models** built on Qwen2.5-VL, InternVL2, LLaVA and related foundations.

The framework aligns timing conventions, reference outputs and experiment records. I used Nsight Systems and Nsight Compute to investigate compute and memory bottlenecks and evaluate the benefits and interference of concurrent execution.

## Optimisation and verification
Parallelising six-camera input preparation reduced median per-frame replay service time from **294.18 ms to 241.58 ms**, a **17.9% reduction**, in an offline development benchmark.

The comparison used four development clips containing 64 frames, alternating baseline and candidate runs. The 384 timed outputs and final histories matched the frozen FP16/compiled reference configuration. This measures the tested replay service, not online driving quality or a production latency guarantee.

## AI-assisted research workflow
I use Claude Code, Codex, Skills and MCP to separate design, implementation and review work. Experiment preregistration, frozen code and parameters, decision logs, evidence checks and milestone acceptance keep conclusions traceable across long development sessions.

This project remains research work; the paper is in preparation. The public summary focuses on verified contributions and experimental scope.

<div class="links"><a href="{{ '/research/' | relative_url }}">Related research →</a><a href="mailto:{{ site.email }}">Discuss the work</a></div>
