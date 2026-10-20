# Scientific contract

1. PROVED requires either a successful Lean check, a deterministic formal-verifier
   certificate, or a reliable primary citation to an established theorem matching the
   exact hypotheses. A title claiming a proof is not an established theorem.
2. A computational observation is not a universal proof. Testing n <= N supports only
   that bounded scope, and even exhaustive finite conclusions require a verified complete
   encoding and checker. A solver exit code alone does not establish either.
3. LLM judgment, consensus and self-reported confidence are not verification.
4. VERIFIED_OPEN requires explicit, credible status evidence, a locator, source identity,
   retrieval date, scope match and freshness check. Uncertainty or conflicting proof claims
   gives OPEN_STATUS_UNVERIFIED. Retrieval of an old survey does not make it recent evidence.
5. Novelty UNKNOWN means research HOLD. GO_TO_LITERATURE_AUDIT authorizes an audit only.
6. Falsification precedes proof search. Preserve exact inputs, code, dependency versions,
   seeds, bounds, logs, output hashes, verifier versions and all failures.
7. Never silently overwrite history. Corrections must supersede immutable records and
   explain why. Hash chains detect accidental changes, not malicious rewriting; Git and
   independent backups are necessary. Consult do_not_replay before every work proposal.
8. Reject fabricated sources, circular support, omitted hypotheses, unsupported equivalent
   formulations and ambiguous mathematical reconstruction. Stop that card and record the
   blocker; continue independent infrastructure work. Missing sources must remain unknown.
9. Failed proof strategies, negative computations, barriers and collisions are permanent
   knowledge. A timeout is not a counterexample or an impossibility theorem. Minimality
   claims require an ordering, bound and completeness certificate.
10. MathForge must not manufacture negative findings to populate directories. Phase 0
    stores an operational replay prohibition and zero purported mathematical failures.

## Enforced boundary and trust

The Phase 0 CLI validates schema, links, source metadata, state transitions, dates and
replay restrictions. It refuses all proof acceptance and research execution. It does not
verify the truth of prose or authenticity of an arbitrary URL. Formal verifier adapters,
axiom auditing (including rejection of sorry/admit), proof-to-statement binding, provenance
signing and source semantic verification are Phase 1 work. No flag bypasses this boundary.
