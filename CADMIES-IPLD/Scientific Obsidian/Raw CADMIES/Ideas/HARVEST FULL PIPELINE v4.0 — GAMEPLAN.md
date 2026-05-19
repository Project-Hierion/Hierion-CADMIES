Status: IN TESTING — phase19-harvest-pipeline-v4
Target: harvest/harvest_full_pipeline.py
Current: Prompt hardening + validation gate fix in progress

---

## 1.0 HIGH-LEVEL FLOW

text

┌─────────────────────────────────────────────────────────────────────────┐
│                       HARVEST FULL PIPELINE v4.0                          │
│                                                                          │
│  STEP 1  →  LOAD conversation from JSON file                             │
│  STEP 2  →  SEARCH mycelium for relevant existing concepts (Willie)      │
│  STEP 3  →  CHUNK conversation (3000 words each, max context integrity)  │
│  STEP 4  →  EXTRACT via Mistral (concepts + poetics + mantras)           │
│  STEP 5  →  TRANSFORM to UniversalScientificConcept schema               │
│  STEP 6  →  SAVE to source_concepts/{human_id}.json                      │
│  STEP 7  →  PRESENT interactive review menu                              │
│  STEP 8  →  VALIDATE approved concepts (BASIC level)                     │
│  STEP 9  →  GENERATE CID (cid_generator)                                 │
│  STEP 10 →  SAVE to blockstore + update index                            │
│  STEP 11 →  CREATE provenance record                                     │
│  STEP 12 →  REPORT results                                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

---

## 2.0 TESTING STATUS

|#|Test|Result|
|---|---|---|
|1|LLM detection (ollama.list().models)|✅ Working|
|2|Robust conversation loader|✅ Working|
|3|Mycelium context search|✅ Working|
|4|Chunking 1282 words → 1 chunk|✅ Working|
|5|Mistral extraction (3 concepts + poetics + mantra)|✅ Working (non-deterministic)|
|6|Transform to UniversalScientificConcept|✅ Working|
|7|Save to source_concepts/|✅ Working|
|8|Interactive review menu (V/L/A/M/S/Q)|✅ Working|
|9|Validation at BASIC level|✅ Configured|
|10|CID generation + blockstore save|⏳ Pending|
|11|Provenance creation|⏳ Pending|
|12|Prompt hardening (object format enforcement)|🔄 In Progress|
|13|No-LLM manual mode with minted_ids filter|✅ Working|
|14|Raw output dump on JSON parse failure|✅ Added|

---

## 3.0 KNOWN ISSUES

|Issue|Status|
|---|---|
|Mistral sometimes returns concepts as strings instead of objects|🔄 Prompt hardened|
|human_id not lowercased (Mistral returns Title_Case)|🔄 Fix pending|
|Non-deterministic extraction — same convo, different results|⚠️ Expected behavior|
|First mint blocked by validation (proof required at STANDARD)|✅ Fixed: BASIC level|

---

## 4.0 NEXT TESTS

1. Re-run with hardened prompt → confirm object format consistency
    
2. Mint 3 concepts to blockstore
    
3. Verify concepts appear in Willie search and Dashboard
    
4. Stop Ollama → test no-LLM path
    
5. Harvest different conversation
    
6. Merge branch to main
    

---

## 5.0 BRANCH STRATEGY

text

main ← phase19-harvest-pipeline-v4 (testing)

- Test on branch until 3 successful mint cycles
    
- Then merge to main and deploy