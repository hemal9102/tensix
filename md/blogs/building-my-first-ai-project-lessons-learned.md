---
title: "Building My First AI Project: Engineering Lessons | TENSIX"
url: https://www.tensix.in/blogs/building-my-first-ai-project-lessons-learned
description: "Lessons from building my first real AI project, a chess engine: why the first version was too slow, how alpha-beta pruning fixed it, and what I learned."
---

[← Back to Blog](https://www.tensix.in/blogs)

AIPythonLearning

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# Building My First AI Project – Lessons Learned

Published on May 20, 2025 · 7 min read

**In plain words**

This is a short story about the first serious AI project I built: a computer program that plays chess. It is for beginner developers, and for business owners curious about how software goes from "it works" to "it works well". The first version was far too slow, and one smarter method made it many times faster. The one takeaway: measure where the real problem is before you try to fix it.

Every developer remembers their first real project — the one that pushed them past tutorials into the messy, beautiful reality of building something that actually works. For me, that was the Chess AI Engine.

## Why Chess?

Chess is a perfect microcosm for AI thinking. It has clear rules, discrete states, and a well-defined win condition. Yet the game tree explodes exponentially — there are more possible chess positions than atoms in the observable universe. Building an AI to navigate that space taught me more about algorithm design than any textbook.

## First Try: Minimax (Checking Every Possible Move)

I started with the classic minimax algorithm: recursively explore all possible moves, assume both players play optimally, and pick the move with the best outcome. Simple in theory. Slow in practice.

The first version was painfully slow — even at depth 3, it took several seconds per move. The game was unplayable.

## The Fix: Alpha-Beta Pruning (Skipping Hopeless Moves Early)

The breakthrough came with alpha-beta pruning. By tracking the best scores found for each player, we can skip entire branches of the game tree that can't possibly improve the result. Suddenly, the same depth that took 8 seconds took under 0.5 seconds.

"Optimization isn't an afterthought — it's the difference between a toy and a tool."

## Lessons I'll Never Forget

**1. Profile before you optimize.** I spent hours optimizing the wrong functions until I ran a profiler and discovered the real bottleneck.

**2. Test incrementally.** Every new feature — move generation, check detection, castling — needs its own test before you build on top of it.

**3. The gap between working and good is huge.** My first working version was a hack. Refactoring it taught me more than the original build.

This project is [on GitHub](https://github.com/hemal9102/ChessAI-Glasses) if you want to explore the code.

[← Why I Chose Automation](https://www.tensix.in/blogs/why-i-chose-automation-over-a-9-to-5) [Next: n8n vs Python Scripts →](https://www.tensix.in/blogs/n8n-vs-python-scripts-when-to-use-which)
