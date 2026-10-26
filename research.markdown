---
layout: page
title: Research
permalink: /research/
eyebrow: Questions, methods & evidence
intro: My work connects numerical systems, distributed learning and AI inference, with an emphasis on resource constraints, reproducible evaluation and practical implementation.
---
<nav class="page-nav" aria-label="Research sections"><a href="#themes">Themes</a><a href="#selected">Selected papers</a><a href="#publications">Publications & talks</a><a href="#patents">Patents</a><a href="#projects-and-funding">Projects & funding</a><a href="#thesis">PhD thesis</a></nav>
<section id="themes"><h2>Research themes</h2><div class="topic-grid"><div><h3>Efficient AI systems</h3><p>Computation graphs, memory reuse, operator optimisation and the timing of multimodal model inference.</p></div><div><h3>Distributed learning</h3><p>Probabilistic synchronisation, heterogeneous clients, resource allocation and energy-efficient learning at the edge.</p></div><div><h3>Agents & cooperation</h3><p>Multi-agent reinforcement learning for crowdsensing, and current engineering work on context retrieval, tools and AI-assisted development.</p></div></div></section>
<section id="selected"><h2>Selected papers</h2>{% include selected-publications.html %}</section>
<section class="section" id="publications"><h2>Publications &amp; talks</h2><p class="meta">Journal entries use the volume/publication year where available; an earlier online-first year may appear in the DOI record. * indicates a corresponding author where marked.</p>
{% assign years = site.data.publications | group_by: 'year' %}{% for year in years %}<h3 class="year-heading">{{ year.name }}</h3>{% for paper in year.items %}<div class="pub-citation">{{ paper.citation | markdownify }}</div>{% endfor %}{% endfor %}
<p class="note">In preparation: <strong>OverDrive: Deadline-Aware Lifecycle Management of VLM-based Driving Model Plans.</strong> See the <a href="{{ '/projects/overdrive/' | relative_url }}">project summary</a> for the experimental scope.</p></section>
<section class="section" id="patents"><h2>Patents</h2>
<p>Four Chinese invention patents, all with Jianxin Zhao as first inventor.</p>
<ul class="pub-list">{% for patent in site.data.patents %}
<li class="pub-item"><h3>{{ patent.title }}</h3><p class="pub-meta">{{ patent.number }}</p></li>
{% endfor %}</ul></section>
<section class="section" id="projects-and-funding"><h2>Projects &amp; funding</h2><p class="meta">Amounts below are total project or sub-project budgets, not personal awards.</p><ul>
<li><strong>NSFC Young Scientists Fund, 2024–2026:</strong> edge-side deep-model training for mobile crowdsensing. Principal investigator; RMB 300,000.</li>
<li><strong>C2CBridge 2, 2024–2026:</strong> German Federal Ministry for Transport project on connected automated mobility. Participant.</li>
<li><strong>Industrial Internet data lake, 2021–2024:</strong> National Key R&amp;D Program sub-project. Core member; RMB 3.518 million.</li>
<li><strong>Edge-side big-data computing, 2022–2026:</strong> NSFC Key Project. Core member; RMB 2.98 million.</li>
<li><strong>Edge intelligent perception, 2022–2025:</strong> NSFC Joint Funds Key Project. Core member; RMB 2.60 million.</li>
<li><strong>Owl:</strong> OCaml Software Foundation grants for maintenance (€10,000, 2024) and open-access book publication ($15,000, 2021).</li>
<li><strong>Connecting Young Scientists at KIT, 2024:</strong> €5,000 grant supporting research exchange with the automotive industry.</li>
<li><strong>China Postdoctoral International Exchange Program, 2021–2023:</strong> fellowship recipient; RMB 400,000.</li>
<li><strong>Databox, 2016–2017:</strong> core contributor to the EPSRC project on privacy-aware personal-data infrastructure (EP/N028260/1; £1.24 million).</li>
</ul></section>
<section class="section" id="thesis"><h2>PhD thesis</h2><p><strong>Optimisation of a Modern Numerical Library: a Bottom-Up Approach.</strong> University of Cambridge, 2020; PhD awarded January 2021.</p><p>The work examines numerical-library implementation and optimisation from operators to higher-level computing abstractions.</p><a href="https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-956.html">Cambridge technical report →</a></section>
