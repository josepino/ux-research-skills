# Affinity diagram / map step by step (detail)

Read when you need to build or facilitate an affinity map (solo, in a team, remote or in person) or solve a concrete problem (orphan notes, huge clusters, a session that stalls).

## Contents
1. What it is and where it comes from
2. Preparation
3. Steps
4. Facilitation and group dynamics
5. Edge cases
6. Common mistakes
7. From affinity to deliverable

## 1. What it is
Grouping observations, quotes or ideas into clusters by natural similarity. Also called affinity mapping, collaborative sorting, snowballing or the **KJ method** (after Jiro Kawakita, a Japanese anthropologist). It is not card sorting: card sorting is a research method for information architecture done with users (NN/g). Affinity mapping is used to analyze research, to organize ideas from ideation and strategy, and to feed personas, empathy maps, journey maps and problem statements. Its main purpose is analyzing existing data, not ideation (Looppanel).

## 2. Preparation
- Set the focus and the questions you want to answer; choose which data goes in (if the focus is one task, only notes from that task).
- Do a **first pass and filter** before the workshop to avoid fatigue; if everything is relevant and there are many people, split into subgroups (NN/g).
- One idea per note, short and specific; **one note = one data point** even if the person said several things at once (UXtweak, IxDF). Include participant ID or a color per participant.
- Metadata to slice later (role, device, country): lets you reorder and see the data from another angle (Condens).
- Group rules and, if the team does not know each other, an icebreaker (Looppanel). Pick the space (wall or Miro/FigJam/Mural): technique matters more than tool (Lyssna).

## 3. Steps (synthesis of NN/g, Condens, IxDF, UXtweak)
1. **Generate notes** (divergent): each person writes alone and fast; NN/g suggests a bounded 5-10 minutes depending on volume. Use colors to tell quotes from observations.
2. **Group**: start grouping by content *before* naming; Condens suggests opening the first cluster with the first note and then adding to it or opening another by similarity. No fixed number of clusters: do not force it.
3. **Name** each cluster with a clear label (ideally user-oriented) and a sentence of what was learned (what this group says).
4. **Hierarchy**: subgroups, or merge narrow groups (IxDF).
5. **Repeat** the grouping from another perspective; the strength of the method is in repetition (Condens). Plan 2-3 refinement rounds (Lyssna).
6. **Zoom out**: relationships between clusters, "lonely" clusters and the hard-to-place notes, which often point to a hidden pattern (Condens).
7. **Prioritize** clusters and define next steps: dot voting if there is no consensus; owners per action; typical actions = research more, open questions, design iterations, how to fix (NN/g).
8. **Document** and save the map; the value is in the conversation as much as in the artifact (NN/g).

## 4. Facilitation and dynamics
- Ask each person to write their notes without influence from the others; dominant participants bias the group (NN/g). Assign different people to lead the discussion (diverge-and-converge).
- Alternative: group in silence first ("silent sorting") and discuss afterwards (Lyssna, Looppanel).
- Synchronous **and** asynchronous sessions: asynchronous work allows processing and reduces groupthink (Condens).
- Include opposing perspectives and do not ignore outliers (NN/g). Involving stakeholders in the mapping builds ownership of the finding.

## 5. Edge cases
- A note that fits two clusters: **duplicate it** and put it in both (NN/g).
- Orphan notes: "Other/Misc" group, or leave them loose and review at the end (IxDF). Look at why they do not fit.
- Small cluster: do not discard it for its size; it may reflect a valuable minority voice (NN/g).
- A giant map that paralyzes: prioritize first, subdivide, or leave with a narrow plan (NN/g).
- Few participants (fewer than 5-6 per group): the cluster describes cases, not generalizable "themes" (Maze criterion for thematic analysis).

## 6. Common mistakes (UserTesting, NN/g)
Lack of preparation; ignoring group dynamics; categories too broad or too narrow; rigid structure; treating the first version as final; not documenting or following up; not measuring the impact of what was implemented afterwards.

## 7. Deliverable
Miro/FigJam-compatible CSV output in `output-formats.md`. To go from a CSV of tagged notes to a theme table with counts per participant and priorities: `scripts/analyze_notes.py`. To communicate: `ux-research-report`; for personas or journey maps: `ux-personas-and-maps`.
