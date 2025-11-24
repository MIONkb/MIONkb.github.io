---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

About
======
{% include mion/introduction.md %}

Education
======
* Ph.D in Electronics Engineer, Fudan University, 2022-2027(expected)
* B.S. in Micro-Electronics, Fudan University, 2018-2022(top 20%)

Open-sourced Projects
======
{% include mion/projects.md %}

Intern Experience
======
<ul>
  {% capture intern %}
    {% include mion/internship.md %}
  {% endcapture %}
  {{ intern | markdownify }}
</ul>
  
Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

Competition
======
{% include mion/competition.md %}


Awards
======
{% include mion/scholar.md %}


Skills
======
{% include mion/skill.md %}

Contact
======
- **Email:** [jhlou22@m.fudan.edu.com](mailto:jhlou22@m.fudan.edu.com)
- **Location:** Zhangheng Road 825, Shanghai, China  张衡路825号,浦东新区
- **GitHub:** [https://github.com/MIONkb](https://github.com/MIONkb)