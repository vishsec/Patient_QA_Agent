1. problem is its i hsrad to keep track of all te patien data since most of it scatterd in lab reports, docs, dischsrge noites , medical lists teh solution is this having an AI agents tarck it for you so when youa sk for parttic;at facts about the patient it can answer you with citations
2. In-Scope 
- [ ] Plan docs spec.md, adr.md, README with checkboxes + "My thoughts"
- [ ] Synthetic corpus generator (PDFs: lab tables, notes, meds, eGFR formula) 
- [ ] Ingestion: PDF parse including tables → rows + chunks, Presidio mask at ingest 
- [ ] Chunking + embeddings into pgvector, measure retrieval 
- [ ] MCP server (own tools: search, get_chunk, run_formula) 
- [ ] LangGraph QA graph + FastAPI endpoint 
- [ ] Verifier gates (quote-in-source, Pydantic, injection, abstain, disclaimer)
- [ ] val harness: golden set, replay fixtures, cost/precision/recall/latency scorecard 
- [ ] packaging: Docker/compose, CI pipeline, README quickstart 
3. simple architecture - ingest _> store _> undertand queries _> retrieve _> answer and cite sources _> verify wth human in loop. 
4. interfaces : 
- [ ] Fast API endpoints 
- [ ] MCP tools
- [ ] LLM wrapper contract
5. Guardrails : 
- [ ] presidio PII masking at ingest its offline and testable. 
- [ ] Injection scanner on retrieved text
- [ ] Pydantic output validation
- [ ] Quote-in-source verifier (deterministic)
- [ ] Abstain threshold (low retrieval score → "I don't know")
- [ ] Medical disclaimer gate (not medical advice, ever)
- [ ] LLM never sees the profile to issue verdicts (if any verdicts exist — it only answers questions here)
6. Non- functional : 
7. Done bars:
same as In-Scope 


8. Descisons made :
- [ ] planted PII on one patient (P002) to check the Masking functionality of the process.  
