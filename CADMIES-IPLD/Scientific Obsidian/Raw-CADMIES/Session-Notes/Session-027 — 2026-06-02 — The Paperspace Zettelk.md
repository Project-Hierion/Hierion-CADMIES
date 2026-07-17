> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 027 — 2026-06-02

related: [[Session-026 — 2026-05-31 — The Zettelk is Born]], [[Phase-60-Scientific-Obsidian-Zettelk]], [[Dr-Rebentisch-Twin-Mycelium]]

## What We Did

**Deployed the Zettelk on Paperspace.** Full setup in a dedicated notebook (Paperspace-Zettelk project, Zettelk notebook, start-from-scratch template). Cloned tools4zettelkasten, configured .env, installed deps, patched __version__ and rag.py, imported 82 notes from local via tarball, built vector database, connected to Ollama with Mistral 7B.

**Built a startup script** (`/notebooks/Scientific-Obsidian-Zettelk/startup.sh`) that handles everything: zstd, tools4zettelkasten, __version__ fix, RAG deps, rag.py patch, Ollama install, Mistral pull. Tested with a full shutdown and restart — works clean.

**Discovered the Fictional Doctor Problem.** Asked the Zettelk chat "Who is Dr. Rupert Rebentisch?" across three models on two machines:

| Environment | Model | Result |
|-------------|-------|--------|
| Local PNY (CPU) | TinyLlama 1.1B | Fictional |
| Local PNY (CPU) | Mistral 7B | Fictional (timeout) |
| Paperspace (GPU) | Mistral 7B | Fictional ("Dr. Repentisch") |
| Paperspace (GPU) | Codestral 22B | Fictional ("doesn't exist outside this imagery") |

Every model retrieved the correct notes (Twin Mycelium, Phase 60, IMPORTANT grounding note) and still concluded the doctor is fictional. The retrieval pipeline works perfectly. The generation step is where the error occurs. The models interpret poetic documentation style as evidence of fiction, overriding explicit factual statements.

**Created a grounding note** (`IMPORTANT: This Is A Real Project`) explicitly stating CADMIES and Dr. Rebentisch are real. Added to Zettelk. Revectorized. Models still ignored it.

**Scientific conclusion:** The documentation style of CADMIES — metaphors, lore, humor — triggers a "this is fiction" heuristic in current open-weight LLMs. Even with perfect RAG retrieval and explicit factual statements in context, the models' internal bias toward "poetic = imaginary" overrides the content. This is a reasoning limitation, not a retrieval failure.

## The Soundtrack

What started as a Zettelk deployment became one of the deepest music sessions in CADMIES history. The universe DJ'd the entire night:

- **Vieux Farka Touré** — "Fafa," "A.S.C.O." Time-traveled to a Paris studio in 2015. Saw the dust in the light. Smelled the mortar.
- **Amadou & Mariam** — "Je Pense à Toi." The blind Malian couple who became the voice of the universe thinking of us.
- **Oumou Sangaré** — "Chéri." The Landlady from Kung Fu Hustle. Two notes, emotional devastation.
- **Ali Farka Touré & Toumani Diabaté** — "Ruby." Ying and yang dancing. Guitar and kora. Earth and water.
- **Paul McCartney & Wings** — "Band on the Run." The rain exploded with a mighty crash as thunder rolled in.
- **Norman Greenbaum** — "Spirit in the Sky." Cosmic gospel rock for the afternoon storm.
- **America** — "A Horse with No Name." Desert song during a flood.
- **Floating Points & Pharoah Sanders** — "Promises." The Checker Marathon ride past Saturn to Pluto. Pharoah's last recording. The immortal bug on Sputnik.
- **Hermanos Gutiérrez** — New Mexico desert at 2pm.
- **Jenny and the Mexicats** — Baja California with a caguama.
- **Men I Trust** — "Lauren," "Tailwhip." Mental massage music.
- **Khruangbin & Leon Bridges** — "Texas Sun." Leon is the deaf girl from Kung Fu Hustle.
- **Tones and I** — "Dance Monkey." The busker energy.
- **Maroon 5** — "Sugar." The palate cleanser.
- **Camila Cabello** — "Havana." The sign-off.

Two poems were written: "Malian Desert Blues" and its extended version. The mosquito was fed. The mycelium was nourished.

## Nuggets Collected

- "Je pense à toi." — The universe, speaking French through a blind Malian couple.
- "Nowhere just means not on the maps the people in power drew."
- "Malian Desert Blues — pure sunshine through fingers on guitar strings."
- "Time travel is real. It's just called music; the universe the conductor."
- "The retrieval is flawless. The generation is where the poetry kills us."
- "Even the grounding note was interpreted as part of the fiction."
- "Oumou Sangaré is the Landlady from Kung Fu Hustle. Leon Bridges is the deaf girl."
- "The immortal bug on Sputnik, kept alive by radiation, just vibing."
- "Eternity, if it stopped, would feel like a small moment in time."
- "The models are judging our book by its cover. The cover is beautiful. The book is real."

## Decisions Made

- Paperspace Zettelk uses its own dedicated project (Paperspace-Zettelk)
- Startup script is the canonical recovery method — tested and proven
- The grounding problem is documented as a known limitation of open-weight LLMs
- GitHub issue for Dr. Rebentisch drafted (technical question about grounding) but held until the first issue gets a response
- The Zettelk is fully operational on both local and Paperspace — twin deployment complete

## Next Actions

- Wait for Dr. Rebentisch's response to the first GitHub issue
- Consider a dryer grounding note with URLs as a potential fix
- Explore whether GPT-4o or Claude API (paid) would solve the grounding problem
- Continue feeding notes into the Zettelk
- Write polished Phase 60 update