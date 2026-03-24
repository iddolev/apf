# Analysis: security-specialist-template vs mykey-security-specialist

Comparison of `instructions/.claude/agent-templates/security-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-security-specialist.md`.

The template is already **very strong** — it has comprehensive sections on threat modeling, input
validation, authentication/authorization, data protection, and dependency security. These are all
generic and well-written.

## Worth incorporating

### 1. Review Methodology (systematic approach)

The mykey version has an 8-step systematic review process: threat model first, input validation,
auth/authz, data protection, error handling, dependencies, configuration, compliance. The template
lacks a structured review workflow. Worth adding as a generic checklist.

### 2. Output Standards (finding report format)

The mykey version defines how to report findings: severity classification
(Critical/High/Medium/Low/Informational), location (file:line:function), description, proof of
concept, remediation, and reference to OWASP/CWE. The template mentions severity in the pipeline
mode section but doesn't have a structured output format. Worth adding.

### 3. Operational Principles

Defense in depth, least privilege, fail secure, zero trust, secure by default, transparency. Most
of these are touched on in the template's subsections, but having them listed as concise guiding
principles at the top level is useful.

### 4. Quality Assurance checklist

5-point checklist: fix doesn't introduce new vulns, backward compat, aligns with existing security
architecture, addresses root cause, controls are testable. Worth adding.

### 5. OWASP Top 10 explicit enumeration

The mykey version lists the OWASP Top 10 (plus SSRF and mass assignment) as a "Security Hardening"
section. The template references OWASP in passing but doesn't enumerate the categories. Could add
as a reference checklist.

## NOT worth incorporating

- MyKey-specific sections (JWT specifics, OTP-based recovery, WebSocket auth, specific rate
  limiting configs, GDPR compliance details) — these belong in `<!-- ADAPT -->` sections, not the
  generic template
- The "pipeline role as optional advisor" framing — the template already handles this differently
  via pipeline awareness (direct vs pipeline mode)
- Verbose memory instructions

## Observation

The template is already one of the best-written templates. The main gap is the lack of a structured
**review methodology** and **output format** — those are the highest-value additions.
