# KO — Worked Examples (manual)

Worked-example study pages for the CTU FEE A4M33KO / B4M33KO course
(Combinatorial Optimization, taught by Zdeněk Hanzálek). One page per
lecture; each page collects the explicit and implicit worked examples
from that deck, with step-by-step solutions synthesised by Claude from
the lectures' stated algorithms. Verify against the original slides
before relying on these for an exam.

This `manual_ko_examples/` directory is the Claude-generated counterpart
to the DeepSeek-driven output at `page/docs/ko/`, produced in parallel so
the two pipelines can be compared.

## Lectures

- [1 — Introduction to Combinatorial Optimization](1_Basic_KO.md) — 5 examples (bin packing FFD, ATSP enumeration, multiway cut, graph isomorphism, clique number)
- [2 — Integer Linear Programming (ILP)](2_ILP.md) — 9 examples (fractional 2-partition, enumerative, B&B, LP-rounding pitfall, shortest-path TU, consecutive-ones workforce, real-estate logical constraints, knapsack-style, Big-M disjunction)
- [3 — Shortest Paths](3_SPT_KO.md) — 6 examples (negative-cycle counterexample, Dijkstra, Bellman–Ford ordering studies, Dow Jones via log-transform DAG, Floyd–Warshall)
- [4 — Network Flows](4_Flows_KO.md) — 6 examples (multiprocessor scheduling via max-flow, Ford–Fulkerson + backward arc, cycle canceling, assignment, Hungarian on 6×6)
- [5 — Knapsack Problem](5_Knapsack.md) — 3 examples (2-approximation, integer-cost DP, integer-weight DP)
- [6 — Traveling Salesman Problem](6_TSP.md) — 8 examples (two HC→TSP reductions, nearest-neighbour, double-tree vs Christofides, 2-opt, 3-opt, 4-opt double-bridge)
- [7 — Scheduling](7_Sched_KO.md) — 13 examples (3-partition feasibility, Bratley B&B, Horn's preemptive EDF, Chetto–Silly–Bouchentouf, McNaughton, LS/LPT tight instances, Graham anomalies, Rothkopf DP, Muntz–Coffman, time-indexed ILP)
- [8 — Constraint Programming](8_CP_KO.md) — 10 examples (Sudoku block prop, REVISE, AC-3, AC-but-infeasible triangle, PC-but-infeasible K₄, GAC vs BC, 4-queens with chronological/FC/MAC, alldifferent via bipartite matching)

**Total:** 60 worked examples across the 8 decks, 67 figures embedded.
