---
permalink: /
title: "Jiahang Lou"
author_profile: false
layout: single
classes: wide
---

<style>
  :root {
    --accent: #2563eb;
    --accent-soft: #eff3ff;
    --text-main: #111827;
    --text-muted: #4b5563;
    --bg: #f9fafb;
    --card-bg: #ffffff;
    --border: #e5e7eb;
  }

  .homepage {
    background: var(--bg);
    color: var(--text-main);
    line-height: 1.6;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }

  .homepage a {
    color: var(--accent);
  }

  .homepage .page-shell {
    max-width: 960px;
    margin: 0 auto;
    padding: 1.5rem 1rem 3rem;
  }

  .homepage header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 1rem;
    background: var(--card-bg);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    border: 1px solid var(--border);
  }

  .homepage .name-block h1 {
    margin: 0;
    font-size: 1.9rem;
    letter-spacing: 0.02em;
  }

  .homepage .name-block h2 {
    margin: 0.1rem 0 0.4rem;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-muted);
  }

  .homepage .name-block .zh-name {
    font-size: 0.95rem;
    color: var(--text-muted);
  }

  .homepage .contact {
    font-size: 0.9rem;
    text-align: right;
    color: var(--text-muted);
  }

  .homepage .contact div {
    margin-bottom: 0.1rem;
  }

  .homepage nav {
    position: sticky;
    top: 0;
    z-index: 10;
    background: rgba(249, 250, 251, 0.9);
    backdrop-filter: blur(8px);
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
  }

  .homepage nav .nav-inner {
    max-width: 960px;
    margin: 0 auto;
    padding: 0.4rem 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    font-size: 0.9rem;
  }

  .homepage nav a {
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: transparent;
    border: 1px solid transparent;
    text-decoration: none;
  }

  .homepage nav a:hover {
    background: var(--accent-soft);
    border-color: var(--accent);
  }

  .homepage section {
    margin-bottom: 1.8rem;
  }

  .homepage h3 {
    margin: 0 0 0.6rem;
    font-size: 1.2rem;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.2rem;
  }

  .homepage .tagline {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
  }

  .homepage .two-col {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: 1.2rem;
  }

  .homepage .card {
    background: var(--card-bg);
    border-radius: 0.9rem;
    padding: 1rem 1.1rem;
    border: 1px solid var(--border);
  }

  .homepage ul {
    margin: 0.3rem 0 0.3rem 1.1rem;
    padding: 0;
  }

  .homepage li {
    margin-bottom: 0.2rem;
  }

  .homepage .edu-item,
  .homepage .exp-item,
  .homepage .pub-item,
  .homepage .award-item {
    margin-bottom: 0.6rem;
  }

  .homepage .edu-title,
  .homepage .exp-title,
  .homepage .pub-title,
  .homepage .award-title {
    font-weight: 600;
  }

  .homepage .meta {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .homepage .label {
    display: inline-block;
    padding: 0.1rem 0.5rem;
    font-size: 0.75rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    margin-left: 0.4rem;
  }

  .homepage .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.3rem;
  }

  .homepage .chip {
    font-size: 0.8rem;
    padding: 0.12rem 0.5rem;
    border-radius: 999px;
    background: #e5f0ff;
  }

  .homepage footer {
    margin-top: 2rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    text-align: center;
  }

  @media (max-width: 720px) {
    .homepage header {
      flex-direction: column;
    }

    .homepage .contact {
      text-align: left;
    }

    .homepage .two-col {
      grid-template-columns: 1fr;
    }
  }
</style>

<div class="homepage">
  <div class="page-shell">
    <header>
      <div class="name-block">
        <h1>Jiahang Lou</h1>
        <h2>Ph.D. Candidate, Fudan University</h2>
        <div class="zh-name">楼佳杭 · 复旦大学集成电路与微纳电子创新学院</div>
        <p class="tagline">
          Research interests: Coarse-grained Reconfigurable Architectures (CGRAs),
          compiler design, polyhedral optimization, heterogeneous systems, and AI compilers.
        </p>
      </div>
      <div class="contact">
        <div>
          <strong>Email:</strong>
          <a href="mailto:jhlou22@m.fudan.edu.com">jhlou22@m.fudan.edu.com</a>
        </div>
        <div><strong>Location:</strong> Shanghai, China</div>
        <div>
          <strong>GitHub:</strong>
          <a href="https://github.com/MIONkb" target="_blank" rel="noopener">MIONkb</a>
        </div>
        <div>
          <strong>Google Scholar:</strong>
          <a href="https://scholar.google.com/citations?user=kqEOgqoAAAAJ&hl=en" target="_blank" rel="noopener">Jiahang Lou</a>
        </div>
      </div>
    </header>

    <nav>
      <div class="nav-inner">
        <a href="#about">About</a>
        <a href="#education">Education</a>
        <a href="#research">Research Interests</a>
        <a href="#publications">Publications</a>
        <a href="#awards">Awards &amp; Competitions</a>
        <a href="#experience">Experience</a>
        <a href="#talks">Conferences</a>
      </div>
    </nav>

    <section id="about">
      <h3>About</h3>
      <div class="two-col">
        <div>
          <p>
            I am a Ph.D. student in Electronics Engineering (EE) at the
            State Key Laboratory of Integrated Circuits and System, Fudan University, supervised by
            Prof. Lingli Wang. My research focuses on
            <strong>coarse-grained reconfigurable architectures (CGRAs)</strong> and
            <strong>compiler design</strong>, with a particular emphasis on
            MLIR-based compilation frameworks, tensor dataflow optimization,
            and heterogeneous CGRA–CPU systems for AI workloads.
          </p>
          <p>
            I have published as the first author at
            <strong>DATE&nbsp;2024</strong> and <strong>DAC&nbsp;2025</strong>,
            and have participated in several national and international
            competitions related to electronic design and GPU programming.
          </p>
        </div>
        <div>
          <div class="card">
            <div class="edu-item">
              <div class="edu-title">Basic Information</div>
              <div class="meta">
                Gender: Male · Age: 25 · Major: Microelectronics
              </div>
            </div>
            <div class="edu-item">
              <div class="edu-title">Current Status</div>
              <div class="meta">
                Ph.D. Candidate (2022–2027), Electronics Information Engineering,
                Fudan University
              </div>
            </div>
            <div class="edu-item">
              <div class="edu-title">Scholarships</div>
              <div class="meta">
                First-class Scholarship (3× during Ph.D., 2× during B.Sc.)
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="education">
      <h3>Education</h3>
      <div class="edu-item">
        <div class="edu-title">
          Ph.D. in Electronics Engineering
        </div>
        <div class="meta">
          Fudan University, Shanghai, China · Sept. 2022 – Jun. 2027 (expected)
        </div>
        <div class="meta">
          Supervisor: <a href="https://sme.fudan.edu.cn/60/3c/c31155a352316/page.htm" target="_blank" rel="noopener">Prof. Lingli Wang</a> (llwang@fudan.edu.cn)
        </div>
        <div>
          Research Focus: CGRA architecture, compiler design, polyhedral model,
          heterogeneous systems, AI compilers, MLIR.
        </div>
      </div>

      <div class="edu-item">
        <div class="edu-title">
          B.Sc. in Microelectronics
        </div>
        <div class="meta">
          Fudan University, Shanghai, China · Sept. 2018 – Jun. 2022
        </div>
      </div>
    </section>

    <section id="research">
      <h3>Research Interests</h3>
      <div class="card">
        <ul>
          <li>Coarse-grained Reconfigurable Architectures (CGRAs)</li>
          <li>Compiler design and MLIR-based compilation frameworks</li>
          <li>Polyhedral model and loop transformations</li>
          <li>Heterogeneous CGRA–CPU and CGRA–GPU systems</li>
          <li>AI compilers and dataflow optimization for DNNs / LLMs</li>
        </ul>
        <div class="chips">
          <span class="chip">CGRA</span>
          <span class="chip">MLIR</span>
          <span class="chip">Polyhedral</span>
          <span class="chip">Heterogeneous SoC</span>
          <span class="chip">AI Compiler</span>
        </div>
      </div>
    </section>

    <section id="publications">
      <h3>Publications</h3>

      <div class="pub-item">
        <div class="pub-title">
          An Agile Deploying Approach for Large-Scale Workloads on CGRA-CPU Architecture
          <span class="label">DATE 2024</span>
        </div>
        <div class="meta">
          Jiahang Lou, et al. · Design, Automation &amp; Test in Europe Conference &amp;
          Exhibition (DATE), Valencia, Spain, March 22–25, 2024.
        </div>
        <div>
          A user-friendly MLIR-based multi-level compiler framework that bridges
          CGRA and RISC-V CPU architectures by automating optimizations and
          hardware–software partitioning for large-scale workloads.
        </div>
      </div>

      <div class="pub-item">
        <div class="pub-title">
          Adora Compiler: End-to-End Optimization for High-Efficiency Dataflow Acceleration
          and Task Pipelining on CGRAs
          <span class="label">DAC 2025</span>
        </div>
        <div class="meta">
          Jiahang Lou, et al. · Design Automation Conference (DAC),
          San Francisco, USA, June 21–25, 2025.
        </div>
        <div>
          A unified framework that bridges user-friendly programming and
          high-performance acceleration for CGRAs through automated loop
          transformations, task/data-flow optimization, and systematic algorithms,
          achieving significant efficiency and scalability in edge computing applications.
        </div>
      </div>

      <div class="pub-item">
        <div class="pub-title">
          CFEACT: A CGRA-based Framework Enabling Agile CNN and Transformer Accelerator Design
          <span class="label">FPL 2024</span>
        </div>
        <div class="meta">
          Yiqing Mao, Xuchen Gao, Jiahang Lou, Yunhui Qiu, Wenbo Yin, Wai-Shing Luk, Lingli Wang. 2024 34th International Conference on Field-Programmable Logic and Applications (FPL)
        </div>
      </div>

      <div class="pub-item">
        <div class="pub-title">
          MDCRA: A Reconfigurable Accelerator Framework for Multiple Dataflow Lanes
          <span class="label">ASAP 2024</span>
        </div>
        <div class="meta">
          Shaoyang Sun, Boyin Jin, Jiahang Lou, Jiangnan Li, Yuhang Cao, Jingyuan Li, Chen Shen, Yuan Dai, Wenbo Yin, Wai-Shing Luk, Lingli Wang. 2024 IEEE 35th International Conference on Application-specific Systems, Architectures and Processors (ASAP)
        </div>
      </div>
    </section>

    <section id="awards">
      <h3>Awards &amp; Competition Experience</h3>

      <div class="award-item">
        <div class="award-title">
          2024 Biren Technology “Flying Cup” GPU Programming Challenge
        </div>
        <div class="meta">
          National First Place · 40,000 RMB · Jul. 2024 – Aug. 2024
        </div>
        <div>
          GPU-based development of AI operators, focusing on performance-optimized
          CUDA kernels and system-level integration.
        </div>
      </div>

      <div class="award-item">
        <div class="award-title">
          2023 “Fudan Electronics Cup” National College Electronic Design Competition
        </div>
        <div class="meta">
          National First Prize · 20,000 RMB · May 2023 – Aug. 2023
        </div>
        <div>
          MLIR-based compiler development for AI model quantization and deployment
          on embedded platforms.
        </div>
      </div>

      <div class="award-item">
        <div class="award-title">
          The 5th National College IC Competition for Innovation and Entrepreneurship (CICC)
        </div>
        <div class="meta">
          Second Prize of National Finals · 15,000 RMB · Mar. 2021 – Aug. 2021
        </div>
        <div>
          Led a team to develop a speech-controlled wireless smart helmet based on
          Xilinx FPGA and IEEE 802.11ah, including hardware and software architecture
          design, low-level I/O, speech recognition accelerator (Verilog),
          RISC-V CPU integration, and SDK software.
        </div>
      </div>
    </section>

    <section id="experience">
      <h3>Intern Experience</h3>

      <div class="exp-item">
        <div class="exp-title">
          GPU Post Silicon Intern – Semi-Custom Business Unit (SCBU)
        </div>
        <div class="meta">
          AMD (Advanced Micro Devices), Shanghai, China · Aug. 2021 – Jan. 2022
        </div>
        <ul>
          <li>
            Developed Python-based tools and infrastructure for post-silicon
            validation and internal server platforms.
          </li>
          <li>
            Completed an SoC project: a runtime power monitor for key on-board
            nodes using STM32 and ADC chips.
          </li>
        </ul>
      </div>
    </section>

    <section id="talks">
      <h3>Conferences &amp; Activities</h3>
      <ul>
        <li>
          <strong>DATE 2024</strong>, Valencia, Spain · Oral presentation of
          DATE paper “An Agile Deploying Approach for Large-Scale Workloads on
          CGRA-CPU Architecture”.
        </li>
        <li>
          <strong>DAC 2025</strong>, San Francisco, USA · Scheduled oral
          presentation of DAC paper “Adora Compiler: End-to-End Optimization for
          High-Efficiency Dataflow Acceleration and Task Pipelining on CGRAs”
          (June 21–25, 2025).
        </li>
      </ul>
    </section>

    <footer>
      Last updated: Nov. 22, 2025 ·
      <a href="https://github.com/MIONkb" target="_blank" rel="noopener">GitHub</a>
    </footer>
  </div>
</div>
