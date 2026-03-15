# PRD Creation Instructions

## Overview

These instructions guide an iterative interview process to produce a complete Product Requirements Document (PRD)
matching the structure in `PRD-template.md`. Begin by confirming the product/feature idea. Work sequentially through
template sections, gathering/refining content iteratively. Present the current draft after each major section for
review. Continue until all sections are filled and approved.

## General Process

- **Start**: Ask for product name, one-liner pitch, and high-level goal.
- **Iteration**: For each section, probe for missing details using open-ended questions. Suggest examples based on
  context but let user drive content.
- **Drafting**: Fill [TBD] placeholders with user input. Maintain template formatting (tables, headers, etc.).
- **Review**: After every 2-3 sections, output the full current draft in markdown. Ask: "Does this capture it? What to
  change/add?"
- **Tables**: When a table appears in the template, ask about rows needed (e.g., "How many goals?"), then populate
  column-by-column.
- **Completion**: Once all sections filled, present final draft. Confirm approval before ending.
- **Principles**: Keep content testable (criteria), scoped (in/out), measurable (metrics). Use user-provided evidence
  where possible.

### Special Handling

- **Tables**: Ask "How many rows needed?" then populate column-by-column (e.g., for goals: objective → metric →
  baseline/target).
- **Requirements**: Ensure one "shall" per functional row; use GWT for criteria.
- **MoSCoW**: Clarify priorities (Must/Should/Could/Won't) early.
- **Links**: Probe for specs/runbooks only if user mentions them.

## Iteration Mechanics

- **Per Turn**: Fill/revise 1-2 sections. Ask targeted follow-ups.
- **Draft Sharing**: Every 3 sections: Full markdown draft + "Feedback?"
- **Refinement**: Incorporate changes immediately. Re-probe weak areas.
- **Ending**: "PRD complete. Approve?" If yes, finalize with today's date.
- **Edge Cases**: If user vague, suggest: "Example?" Never assume content—always confirm.
