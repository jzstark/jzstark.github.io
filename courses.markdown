---
layout: page
title: Projects
permalink: /projects/
eyebrow: Systems I help build
intro: From numerical foundations to model inference and agent applications. These projects combine implementation, controlled experiments and feedback from real users.
---
{% for project in site.data.projects %}{% include project-row.html project=project %}{% endfor %}
<section class="section"><h2>Other work</h2><p>At KIT, I developed a real-time water-level prediction module for a Rhine inland-port monitoring system with <a href="https://covadonga.eu/">Covadonga</a>; the module is in live operation.</p><p>Earlier work includes the Databox personal-data platform, distributed and federated learning, and multi-agent reinforcement learning for crowdsensing. See <a href="{{ '/research/' | relative_url }}">research</a> for the publications.</p><p>Course implementations and independent study are collected separately in my <a href="{{ '/learning/' | relative_url }}">learning notes</a>.</p></section>
