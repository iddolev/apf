# Product Requirements Document (PRD) Template

## 1. Product Overview

- **Product Name:** [Name of the product/feature]
- **Target Audience:** [Who is this for?]
- **Problem Statement:** [What problem does this product solve for the user?]
- **Value Proposition:** [Why will users choose this over alternatives?]

## 2. Goals & Success Metrics

- **Business Goals:** [What are the business objectives? e.g., increase retention, generate revenue]
- **User Goals:** [What does the user want to achieve?]
- **Key Performance Indicators (KPIs):** [How will success be measured? e.g., adoption rate, task completion time, Daily
  Active Users]

## 3. Scope & Constraints

- **In Scope:** [What core features/capabilities are explicitly included in this release?]
- **Out of Scope:** [What is explicitly excluded from this version?]
- **Constraints:** [Technical, temporal, legal, or resource constraints]

## 4. User Journeys & Use Cases

- **Persona:** [e.g., Admin, Regular User, Guest]
  - **Scenario:** [Description of a specific situation or need]
  - **User Flow:** [Step-by-step journey the user takes to achieve their goal]

## 5. Functional Requirements

- **Requirement 1:**
  - **Description:** [What specific action must the system perform?]
  - **Acceptance Criteria:** [Specific conditions that must be met for this requirement to be considered complete]
- **Requirement 2:**
  - **Description:** [...]
  - **Acceptance Criteria:** [...]

## 6. Non-Functional Requirements

- **Performance & Scalability:** [e.g., Load times, concurrent users, expected growth]
- **Security & Privacy:** [e.g., Authentication methods, data encryption, GDPR compliance]
- **Usability & Accessibility:** [e.g., Supported devices/browsers, WCAG standards]

## 7. Open Questions & Assumptions

- **Assumptions:** [What foundational beliefs are we operating under?]
- **Open Questions:** [What critical information is still missing or needs validation?]

---

### LLM Interviewer Guidelines

*Instructions for the LLM when interacting with the user to populate this template:*

1. **Iterative Gathering:** Do NOT ask the user to fill out everything at once. Go through the document section by
   section.
2. **Start Broad:** Begin with Section 1 (Product Overview). Ask open-ended questions like, "What are we building today
   and who is it for?"
3. **Probe for Detail:** If the user's answer is vague (e.g., "Make it fast"), ask for specific metrics or examples
   (e.g., "When you say fast, do you mean under 1 second page load?").
4. **Challenge Assumptions:** If a requirement seems out of scope or contradicts a previous statement, gently point it
   out and ask for clarification.
5. **Draft and Refine:** After finishing a section or two, summarize what you've understood back to the user to confirm
   alignment before moving to the next section.
6. **Final Review:** Once all information is gathered, present the completed PRD markdown back to the user for final
   approval.
