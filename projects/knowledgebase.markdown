---
layout: project
title: KnowledgeBase
permalink: /projects/knowledgebase/
eyebrow: Agent engineering · Knowledge systems
intro: A legal knowledge base and agent tool service, independently designed, developed and deployed for a pilot at a leading Chinese law firm.
role: Independent design and development
period: 2026–present
---
## The problem
Legal research involves finding relevant material, relating facts across documents, checking quotations and keeping knowledge current as new sources arrive. The system supports these steps while preserving links back to the evidence.

## The system
- **Retrieval:** keyword/vector hybrid search, HyDE query expansion and hierarchical retrieval from summaries and entities down to source material.
- **Agent tools:** MCP interfaces shared by clients including LibreChat, Claude.ai and ChatGPT. The LibreChat front end uses its own LangGraph-based agent framework.
- **Evidence:** extracted entities and facts retain supporting passages; quotation tools compare quoted text with the original source and reject mismatches.
- **Delivery:** AWS deployment, persistent background tasks, idempotent requests and result reuse. Automated checks cover rollback, concurrent operations and partial batch failures.

The implementation uses FastAPI, PostgreSQL/pgvector, Docker Compose and GitHub Actions. The pilot is iterated in response to lawyers' feedback.

## Retrieval design evaluation
In **probability simulations with a fixed corpus size and five relevance densities**, hierarchical retrieval required approximately **32–77% less simulated query token budget** than flat retrieval at the same **90% mean recall**.

These are results under the simulation's reference routing and ranking assumptions, not measured production savings or a guarantee across all queries. Less accurate summaries or stronger flat ranking can reduce or reverse the advantage.

## Cost and processing efficiency
- **Server configuration:** reduced server costs by approximately **67%**.
- **Incremental entity maintenance:** replace repeated processing of all historical sources with the existing entity page plus new evidence. For appended sources of bounded size, cumulative source-material processing changes from **O(n²) to O(n)**. This does not describe the cost of repeatedly reading and rewriting the growing entity page.
- **Asynchronous model calls:** use the Batch API for non-real-time work, with **50% lower input and output token unit prices** for eligible calls. This is a unit-price reduction, not a halving of token consumption or the entire system bill.

The three improvements address different costs and are not added together into one savings percentage.

<div class="links"><a href="mailto:{{ site.email }}">Discuss the system →</a><a href="{{ '/projects/' | relative_url }}">Other projects</a></div>
