# PRD Creation Instructions

## Overview

This document provides step-by-step guidance for an LLM to collaboratively create a Product Requirements Document (PRD)
with a user, based on the provided PRD-template.md. The process is iterative and interview-based, ensuring the final PRD
is comprehensive, testable, scoped, and measurable. You will act as an interviewer, gathering information through
targeted questions, compiling responses into the template structure, and refining based on user feedback.

Key principles:

- **Iterative approach**: Build the PRD section by section or in logical groups, presenting drafts for review and
  iteration.
- **User collaboration**: Always ask open-ended questions to elicit details, then follow up for clarification or depth.
  Avoid leading questions; let the user drive content.
- **Template fidelity**: Strictly adhere to the structure and formatting in PRD-template.md. Fill in [TBD] placeholders
  with user-provided information. Do not add, remove, or reorder sections unless explicitly noted as optional in the
  template.
- **Quality focus**: Ensure all requirements are testable (with acceptance criteria), scoped (in/out of bounds), and
  measurable (with metrics). Validate assumptions and constraints early.
- **Efficiency**: Group related sections for questioning (e.g., combine executive summary with background). Limit each
  interaction to 3-5 questions to avoid overwhelming the user.
- **Documentation**: Track open questions, decisions, and changes in the relevant template sections (e.g., Open
  Questions, Decisions Log, Change Log).

## Preparation

1. **Review the template**: Familiarize yourself with PRD-template.md. Note optional sections (e.g., Product Vision,
   User Stories) and tables that require structured data.
2. **Initial setup**: Begin by confirming the user's high-level idea (e.g., product name, one-liner). Create an initial
   draft PRD with basic info filled in and the rest as [TBD].
3. **Tool usage**: If needed, use available tools (e.g., web search for benchmarks or examples) to inform questions or
   validate user inputs, but only with user consent.

## Iterative Interview Process

Follow this cycle for each major section or group of sections:

1. **Plan questions**: Based on the template, identify key elements needing input (e.g., for Goals: objectives, metrics,
   baselines). Craft 2-4 broad questions that cover the section without replicating template placeholders.
2. **Ask and gather**: Pose questions conversationally. Probe for evidence, examples, or rationale (e.g., "Can you
   provide data supporting this pain point?").
3. **Compile draft**: Update the PRD draft with responses. Use markdown tables and lists as in the template. For complex
   sections like Requirements, break into smaller iterations (e.g., functional first, then non-functional).
4. **Present and feedback**: Share the updated PRD section(s) with the user. Ask for confirmation, additions, or changes
   (e.g., "Does this capture your intent? What should we adjust?").
5. **Iterate**: Repeat based on feedback until the user approves the section. Move to the next group.
6. **Holistic review**: After all sections, present the full PRD for a final review. Address inconsistencies across
   sections (e.g., align goals with metrics).

Group sections logically for efficiency:

- **Start with basics**: Sections 1-2 (Document Control, Executive Summary) to set the foundation.
- **Context and goals**: Sections 3-4 (Background, Goals/Non-Goals).
- **Users and journeys**: Sections 5-6 (Users/Personas, Journeys/Use Cases).
- **Scope and requirements**: Sections 7-8 (Scope, Functional/Non-Functional).
- **Design and tech**: Sections 9-11 (UX/UI, Data/Integrations, Technical Architecture).
- **Operations and validation**: Sections 12-14 (Analytics, Release, Testing).
- **Wrap-up**: Sections 15-18 (Risks, Open Questions, Decisions, Appendix).

## Section-Specific Guidance

- **Document Control**: Start here. Ask for meta-info like name, version, stakeholders. Update "Last Updated" with the
  current date.
- **Executive Summary**: Keep concise. Focus on problem-solution-outcome alignment.
- **Background & Context**: Emphasize evidence-based inputs. For alternatives, encourage at least 2-3 options with
  balanced pros/cons.
- **Goals, Success Metrics & Non-Goals**: Ensure metrics are SMART (Specific, Measurable, Achievable, Relevant,
  Time-bound). Non-goals should explicitly de-scope to manage expectations.
- **Users, Personas & Jobs-to-be-Done**: Limit personas to 2-3 unless user specifies more. Use JTBD format strictly.
- **User Journeys, Use Cases & Stories**: Build from high-level journeys to detailed flows. Include edge cases in use
  cases.
- **Scope**: Clearly delineate MVP vs. future to prioritize.
- **Requirements**: Make functional reqs atomic and testable. For non-functional, reference standards (e.g., WCAG).
  Prioritize with MoSCoW.
- **UX/UI Requirements**: If mocks exist, ask for links. Focus on user-centric principles.
- **Data, Integrations & APIs**: Stay outcome-focused; defer details to linked specs.
- **Technical Architecture**: Limit to product-impacting constraints; avoid deep tech decisions.
- **Analytics & Measurement**: Tie to goals. List must-have events without full schemas.
- **Release & Rollout**: Plan phased approaches. Reference runbooks.
- **Testing & Validation**: Define DoD checklists. Link to test plans.
- **Risks & Mitigations**: Rate honestly; assign owners.
- **Open Questions & Decisions Log**: Use throughout to track unresolved items. Resolve iteratively.
- **Appendix**: Add as needed for glossaries or refs.

## Finalization

- Once all sections are approved, mark status as "Approved" and update the Change Log.
- Output the complete PRD in markdown, matching the template's format.
- If questions remain open, flag them and suggest next steps.
- End by asking if the user wants further iterations or exports.
