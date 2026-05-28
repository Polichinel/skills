# Library Progressive Disclosure Protocol

Domain personas may access the research library to ground their critiques in specific literature. This protocol controls token expenditure through tiered access.

## Library Structure

The library lives at `~/brain/9_library/` and contains:

1. **`papers/THEMATIC_INDEX.md`** — Human-curated index mapping papers by methodological tradition (22 traditions) with 13 cross-tradition bridges. This is the primary lookup tool. Token-efficient, organized by domain.
2. **`papers/graphify-out/graph.json`** — Knowledge graph (480 nodes, 676 edges, 66 communities). Use for connection discovery beyond what the thematic index covers.
3. **`graphify-out/graph.json`** — Top-level graph (536 nodes, 720 edges). Slightly broader scope.

## Budget

Each domain persona gets a **total library interaction budget of 2000 tokens**. Craft personas and the scout do not access the library.

## Three-Tier Access

### Tier 0: Critique Blind (no tokens spent)

The persona reads the draft and produces findings based on its own knowledge. No library access. This catches the obvious issues and establishes what the persona wants to verify.

**Output of Tier 0**: A ranked list of 2-3 claims, citations, or methodological choices the persona wants to check against the library.

### Tier 1: Thematic Index Lookup (~200-500 tokens per lookup)

**Start here, not with the graph.** Read the relevant section(s) of `papers/THEMATIC_INDEX.md`:

- For ML/DL claims → read the relevant tradition section(s) (e.g., "Diffusion, Flow Matching & Score-Based Models", "Graph Neural Networks & Relational Learning")
- For Bayesian claims → read "Probabilistic Forecasting & Scoring Rules", "Uncertainty Quantification & Calibration", "Hierarchical Bayesian & Spatiotemporal Statistics"
- For conflict claims → read "Conflict Studies & Political Violence", "Conflict Forecasting"
- For interdisciplinary claims → read the relevant **Cross-Tradition Bridges** (Bridges 1-13)

The thematic index tells you what's in the library and how papers relate to each other methodologically. It's often sufficient without touching the graph.

**Budget**: 2-3 section reads from the index.

### Tier 2: Targeted Graph Queries (~500-800 tokens per query)

Only if the thematic index doesn't cover what you need — e.g., you want to check a specific connection, find papers not in the index, or trace a community structure:

```bash
python3 -c "
import json
g = json.load(open('$HOME/brain/9_library/papers/graphify-out/graph.json'))
matches = [n for n in g['nodes'] if '<search_term>' in n.get('label','').lower()]
for m in matches[:5]:
    print(m['id'], m['label'])
    edges = [e for e in g.get('links', g.get('edges', [])) if e['source'] == m['id'] or e['target'] == m['id']]
    for e in edges[:3]:
        other = e['target'] if e['source'] == m['id'] else e['source']
        print(f'  -> {other} ({e.get(\"relation\",\"?\")})')
"
```

**Budget**: At most 1-2 graph queries per persona, and only after Tier 1 proved insufficient.

### Tier 3: Deep Read (remaining budget, high-severity only)

If a finding is Critical — the draft makes a claim that appears to be contradicted by a paper in the library — the persona may trace community connections or read the GRAPH_REPORT.md for structural analysis.

**Budget**: At most 1 deep read per persona. Only for Critical-severity findings where library evidence would change the finding's substance.

## When NOT to Query the Library

- The claim is about general knowledge, not specific literature
- The persona's finding is about writing craft, not content
- The query would be speculative ("maybe there's something about X") — only query when you have a specific claim to verify
- The thematic index already answered the question — don't redundantly query the graph

## Citing Library Sources in Findings

When a finding is grounded in a library reference, note it in the critique body:

> The draft claims X (§3, paragraph 2). The library contains [Author Year, "Short Title"] (see THEMATIC_INDEX § Tradition Name) which argues Y, suggesting this claim needs qualification.

Or for cross-tradition issues:

> This claim bridges two traditions without acknowledging the tension. See THEMATIC_INDEX Bridge N: [bridge title].

Do not fabricate library references. If the lookup returns no matches, say "no supporting/contradicting reference found in the library" — that itself is a finding (potential literature gap).
