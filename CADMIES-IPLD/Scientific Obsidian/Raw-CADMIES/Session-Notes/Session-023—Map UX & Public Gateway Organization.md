> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 023 — Map UX & Public Gateway Organization

## Pending Work

### Map Improvements (mycelium_map.html)
1. **Circle Spacing:** Nodes should not overlap. Add force collision with auto-spacing.
   Manual drag override allowed.
2. **Click-to-Highlight (Restore):** Click a concept → connected nodes stay visible,
   non-connected fade. This feature existed but broke somewhere.
3. **Legend Domain Filter:** Click a domain in the legend → all concepts in that domain
   stay bright. Connected concepts from other domains ghost at partial opacity.
   Edges between domains remain visible.
4. **Gradient Edge Fade:** When a node is clicked, edges radiating from it are bright
   at the center and gradually fade toward the connected node. Ripple effect.

### Public Gateway (index.html)
5. **Domain Sections:** Group 581 concept cards under the 15 canonical domain headers.
   Search and filters still work globally. Bookstore layout instead of firehose.

## Notes
- All front-end work. No backend changes needed.
- The map data is solid — just needs UX love.
- Terminator pipeline v4.2.2 is proven and doesn't need changes.