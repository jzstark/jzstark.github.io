---
layout: default
title: AI Systems, Agent Engineering & Open Source
---
<section class="hero" aria-labelledby="intro-title">
  <div>
    <p class="eyebrow">Research meets implementation</p>
    <h1 id="intro-title">Jianxin Zhao</h1>
    <p class="role">AI systems. Agent engineering.<br>Open-source computing.</p>
    <p class="intro">I work on efficient model inference, agent systems and numerical computing. I lead the <a href="https://github.com/owlbarn/owl">Owl</a> open-source project and build systems that connect research ideas with practical applications.</p>
    <p class="intro">PhD in Computer Science, University of Cambridge.<br>Research experience at KIT and Beijing Institute of Technology.</p>
    <div class="links"><a class="button" href="{{ '/files/cv.pdf' | relative_url }}">Download CV <span aria-hidden="true">↗</span><span class="sr-only"> (English PDF)</span></a><a href="https://github.com/jzstark">GitHub</a><a href="mailto:{{ site.email }}">Email</a></div>
  </div>
  <figure class="portrait"><img src="{{ '/images/stark.jpg' | relative_url }}" alt="Jianxin Zhao" width="230" height="230" fetchpriority="high"><figcaption>Researcher, engineer<br>and open-source maintainer.</figcaption></figure>
</section>
<dl class="facts" aria-label="At a glance"><div><dt>25+</dt><dd>Research publications</dd></div><div><dt>2017–</dt><dd>Owl core development</dd></div><div><dt>4</dt><dd>First-inventor patents</dd></div></dl>
<section class="section" aria-labelledby="selected-work"><div class="section-heading"><h2 id="selected-work">Selected work</h2><a href="{{ '/projects/' | relative_url }}">All projects →</a></div><div>{% for project in site.data.projects %}{% include project-row.html project=project %}{% endfor %}</div></section>
<section class="section" aria-labelledby="books-home"><div class="section-heading"><h2 id="books-home">Books &amp; explanations</h2><a href="{{ '/books/' | relative_url }}">All books →</a></div><div class="book-grid">{% for book in site.data.books limit:2 %}<article class="book-preview">{% include book-cover.html book=book %}<div><p class="book-venue">{{ book.publisher }} · {{ book.year }}</p><h3>{{ book.title }}</h3><p>{{ book.subtitle }}</p><a class="text-link" href="{{ '/books/' | relative_url }}#{{ book.id }}">About the book →</a></div></article>{% endfor %}</div></section>
<section class="section" aria-labelledby="research-home"><div class="section-heading"><h2 id="research-home">Selected research</h2><a href="{{ '/research/' | relative_url }}">Research &amp; papers →</a></div>{% include selected-publications.html %}</section>
<section class="section about-short" aria-labelledby="beyond-work"><div><p class="eyebrow">Beyond the code</p><h2 id="beyond-work">Curiosity, in practice.</h2></div><div><p>I enjoy explaining systems as much as building them: through open-source documentation, books, teaching and collaboration. Away from the screen, I practise kendo, cycle and explore new places.</p><a class="text-link" href="{{ '/about/' | relative_url }}">More about me →</a></div></section>
