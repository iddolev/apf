# API Integration Tests: Common Strategy

## The Problem

Unit tests that mock external API calls (e.g., LLM providers) verify control flow — success paths, error handling, timeouts — but they **cannot catch real API contract changes**. Mocks silently accept any parameter you pass, so when a provider deprecates or renames a parameter (e.g., OpenAI changing `max_tokens` to `max_completion_tokens`), mocked tests pass green while the real API rejects your calls.

## Three-Tier Test Strategy

| Tier | Uses real APIs? | Deterministic? | Cost | What it catches |
|------|-----------------|----------------|------|-----------------|
| **Unit tests** (mocked) | No | Yes | Free, fast | Logic errors, control flow, error handling |
| **Integration tests** (real API calls) | Yes | No — depends on providers | API credits, 5-10s per call | Wrong parameters, SDK breaking changes, auth failures, model deprecation |
| **UAT** (manual) | Yes | No — human judgment | Time | End-to-end user-observable behavior |

Each tier catches a different class of bug. Skipping the integration tier leaves a gap where SDK/API contract changes go undetected until manual testing or production.

## API Keys: Required, Not Optional

These integration tests require real API keys. The keys should **never** be committed to git.

Where keys come from:

- **Locally**: system environment variables or `.env` file (which is in `.gitignore`)
- **CI/CD**: Repo secrets, injected as environment variables in the workflow
  - On GitHub: Settings > Secrets and variables > Actions 
  - On GitLab: Settings > CI/CD > Variables (toggle "Masked" to hide values in logs, "Protected" to limit to protected branches)

A critical design decision: **missing keys should fail the test, not skip it.** If the application requires API keys to function, then their absence is a configuration error that must be caught. The `@pytest.mark.skipif(not os.getenv("KEY"), ...)` pattern is appropriate for optional features — but API access is not optional for an LLM application.

```python
# Correct: fails if environment is misconfigured
@pytest.mark.integration
async def test_openai_real_call():
    result = await call_provider(Provider.OPENAI, "Say hello", get_settings())
    assert result.error is None
    assert result.content is not None

# Wrong: silently hides a broken environment
@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No API key")
async def test_openai_real_call():
    ...
```

The `@pytest.mark.integration` marker exists for **speed separation** (so you can run fast unit tests independently), not to excuse missing configuration.

## When to Run API Integration Tests in CI/CD

Running integration tests on every push/PR has real downsides:

- **Cost**: each run burns API credits (real calls to paid providers)
- **Latency**: adds 5-30 seconds depending on provider response times
- **Flakiness**: provider outages, rate limits, or network issues cause CI failures unrelated to your code
- **Noise**: a typo-fix PR doesn't need to validate API contracts

### Recommended approach: non-blocking nightly health check

Integration tests with external APIs should **never block** pushes, PRs, or merges. 
The reason: even after a failure is detected, the fix may take time, and depend on external providers.
Blocking all work in the meantime is worse than the bug itself. 
Instead, integration tests run as a **nightly health check** that notifies developers when something breaks, 
so they can address it manually.

| Trigger | What runs | Blocks merges? | On failure |
|---------|-----------|----------------|------------|
| Every PR/push | Unit tests only (`pytest -m "not integration"`) | Yes | PR cannot merge |
| Nightly (scheduled) | Integration tests (real API calls) | No | Email report sent to developers |
| Manual dispatch | Integration tests | No | Email report sent to developers |

### Why non-blocking?

- SDK breaking changes and API deprecations don't happen hourly — 
  nightly detection is fast enough
- Provider outages are **not your bug** — they shouldn't stall your team's work
- The fix for a broken API contract (parameter rename, model deprecation) requires investigation and a code change — 
  blocking merges doesn't make that happen faster
- On most days, all providers respond correctly and **no notification is sent** — silence means healthy

### Notification behavior

- **All tests pass**: no notification. Silence means healthy.
- **One or more tests fail**: email report sent to configured developers with this info:
  - Which provider(s) failed
  - The error message returned
  - Timestamp of the run
  - Link to the full CI/CD job log

This is a **monitoring** concern, not a **gating** concern. 
Think of it like an uptime alert, not a build gate.

### GitHub Actions example

```yaml
name: API Health Check

on:
  # Nightly at 2:00 AM UTC
  schedule:
    - cron: '0 2 * * *'

  # Manual trigger
  workflow_dispatch:

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -m "not integration" -x

  integration-tests:
    # Only run on schedule or manual trigger
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -m integration --tb=short --junitxml=report.xml
        continue-on-error: true
        id: tests

      - name: Send failure report
        if: steps.tests.outcome == 'failure'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "API Health Check FAILED - ${{ github.repository }}"
          to: ${{ secrets.DEVELOPER_EMAIL }}
          from: CI/CD Health Check
          body: |
            One or more API integration tests failed.

            Repository: ${{ github.repository }}
            Branch: ${{ github.ref_name }}
            Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
            Time: ${{ github.event.head_commit.timestamp || 'scheduled run' }}

            Please review the job log and address the failing provider(s).
```

Note: `continue-on-error: true` ensures the workflow proceeds to the email step even when tests fail. 
The condition `if: steps.tests.outcome == 'failure'` means the email is **only sent when something breaks**.

For email via Gmail, you'll need an App Password (not your regular password). 
Alternatively, you can use the plantoform (e.g. GitHub) built-in notification for failed workflows

- On GitHub: Settings > Notifications
- On GitLab: Settings > Integrations > Pipeline status emails (sends to configured recipients on pipeline failure)

or replace the email step with a Slack webhook, Teams notification, etc.

### GitLab CI/CD example

```yaml
stages:
  - unit-test
  - integration-health

unit-tests:
  stage: unit-test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest -m "not integration" -x
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

integration-health-check:
  stage: integration-health
  image: python:3.12
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
    OPENAI_API_KEY: $OPENAI_API_KEY
    GOOGLE_API_KEY: $GOOGLE_API_KEY
  script:
    - pip install -r requirements.txt
    - pytest -m integration --tb=short --junitxml=report.xml || FAILED=true
    - |
      if [ "$FAILED" = "true" ]; then
        echo "Integration tests failed — sending notification"
        # Use GitLab API or curl to send email/Slack notification
        curl -X POST "$SLACK_WEBHOOK_URL" \
          -H 'Content-type: application/json' \
          -d "{\"text\": \"API Health Check FAILED in $CI_PROJECT_NAME. See: $CI_PIPELINE_URL\"}"
      fi
  allow_failure: true  # Never blocks the pipeline
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"    # Nightly via Pipeline Schedules
    - if: $CI_PIPELINE_SOURCE == "web"         # Manual trigger from UI
  artifacts:
    when: always
    reports:
      junit: report.xml
```

**GitLab setup:**

- **Secrets**: Settings > CI/CD > Variables (toggle "Masked" and "Protected" for API keys)
- **Nightly schedule**: CI/CD > Schedules > New Schedule (set cron expression `0 2 * * *`)
- **`allow_failure: true`**: marks the job with a warning icon but never blocks the pipeline
- **Notifications**: GitLab can email on pipeline failure (Settings > Integrations > Pipeline emails), or use a Slack/webhook integration as shown above

## Summary

1. **Mock-based unit tests** are necessary but insufficient — they can't catch real API contract changes
2. **Integration tests with real API calls** fill the gap between mocks and manual testing
3. **API keys are required infrastructure** — missing keys should fail, not skip
4. **Run integration tests nightly as a non-blocking health check** — on failure, email developers; on success, stay silent
5. **Never block PRs or merges on integration test results** — these are monitoring alerts, not build gates
6. **Store keys in the repo's secrets or CI/CD variables** for CI, environment variables for local development — never in git
