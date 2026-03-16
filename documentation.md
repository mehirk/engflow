# EngFlow — Product Documentation

**Version:** 1.0 · **Status:** Active Development · **Last Updated:** March 2026

---

## 1. Executive Summary

**EngFlow** is a developer analytics platform that transforms GitHub activity into actionable engineering performance insights.

Think of it as Google Analytics for engineering teams — instead of tracking page views and bounce rates, EngFlow tracks commits, pull requests, CI runs, and review cycles. It answers the questions engineering leaders ask every week but currently have no clean way to answer.

EngFlow is not a code hosting platform, a project management tool, or a developer surveillance system. It is an intelligence layer that sits above GitHub, collects engineering signals, and surfaces meaningful patterns about how software development is flowing through a team.

---

## 2. Problem Statement

Engineering leaders — managers, tech leads, CTOs — consistently face the same gap: they have access to GitHub, but GitHub is not an analytics tool. To understand engineering health, they currently have to manually check dashboards, export CSVs, build one-off scripts, or rely on gut feel.

This means critical signals arrive late or not at all:

- A repository that has been slowing down for three weeks goes unnoticed until a release slips.
- Pull requests waiting 72 hours for review are invisible until someone complains.
- CI failures trending upward don't trigger any alert until they become a crisis.
- No one knows which contributors are becoming bottlenecks, and which repos are silently stagnant.

EngFlow solves this by automatically collecting engineering activity and computing metrics that make these patterns visible before they become problems.

---

## 3. Product Vision

> EngFlow converts raw GitHub engineering activity into measurable signals about how software development is flowing.

The long-term ambition is a single platform where any engineering organization can connect their GitHub repositories and immediately gain a clear, accurate picture of delivery speed, review health, CI reliability, and contributor activity — with no manual setup, no data exports, and no dashboards to maintain.

In the short term, the goal is simpler: build a pipeline that reliably ingests commit data, processes it into structured records, computes useful metrics, and presents them through a clean API or dashboard.

---

## 4. Target Users

EngFlow is built for the people who need to understand how engineering work is flowing, not the people doing the engineering work itself.

**Engineering Managers** need to understand delivery pace, identify bottlenecks, and have data-backed conversations about team health without manually digging through GitHub.

**Tech Leads** need to understand code review load, CI reliability, and whether their team's velocity is improving or degrading over sprints.

**CTOs and Startup Founders** need a high-level picture of engineering activity across repositories — which teams are shipping, which are stalled, and where investment is actually going.

**Developer Productivity Teams** need to track DORA-aligned metrics (deployment frequency, lead time, change failure rate, time to restore) and run experiments to improve engineering efficiency.

---

## 5. Goals and Non-Goals

### Goals

- Ingest engineering activity from GitHub (commits, pull requests, reviews, CI runs)
- Store raw event data reliably with full reprocessing capability
- Process raw data into clean, normalized records via a medallion pipeline
- Compute meaningful engineering metrics at the repository and organization level
- Expose metrics through a queryable API and basic visualization layer
- Design for incremental expansion: start with commit metrics, grow to full engineering intelligence

### Non-Goals

- Replacing GitHub as a code hosting platform
- Building a project management or ticketing system
- Measuring individual developer output in a punitive or surveillance-oriented way
- Shipping a production-grade, enterprise analytics suite in V1
- Supporting VCS platforms other than GitHub in the first version

---

## 6. Feature Overview

### 6.1 Repository Connection

Users connect one or more GitHub repositories to EngFlow. This involves authorizing a GitHub token, specifying repository targets, and triggering an initial historical backfill followed by ongoing scheduled ingestion.

Support for organization-level connection is planned, allowing all repositories in a GitHub organization to be ingested with a single authorization.

### 6.2 Commit Analytics

The foundation of EngFlow. Every commit is ingested, normalized, and surfaced through metrics including daily and weekly commit volume, active contributor count, commits per contributor, commit velocity trend over time, and first-time vs. returning contributor identification.

### 6.3 Pull Request Analytics _(V2)_

Once a PR is opened, merged, or closed, EngFlow captures it and computes PR open rate and merge rate, average time from open to merge, review latency (time from PR open to first review), PR age distribution (how long open PRs have been sitting), and reviewer workload distribution.

### 6.4 Code Review Intelligence _(V2)_

A sub-feature of PR analytics that specifically tracks the review cycle: who is reviewing and how often, how long reviews take to arrive, review depth (number of review cycles before merge), and identification of review bottlenecks at the contributor or team level.

### 6.5 CI / Workflow Analytics _(V3)_

Tracks GitHub Actions workflow runs: CI success and failure rates per repository, average workflow duration over time, failure trend detection, and flaky test signals (workflows that alternate pass/fail without code changes).

### 6.6 Engineering Health Dashboard _(V2–V3)_

A summary view across repositories showing which repos are active vs. stagnant, overall delivery velocity trend, flagged anomalies (e.g. CI failure rate spiked this week, PR merge time doubled), and contributor concentration risk.

### 6.7 Alerts and Anomaly Detection _(V4)_

Configurable alerts when metrics cross thresholds: PR aging beyond a configured limit, CI success rate drops below a threshold, commit activity drops to near-zero in an active repository, and contributor activity disappearing unexpectedly.

### 6.8 DORA Metrics _(V4)_

Alignment with the four DORA indicators that are industry-standard proxies for software delivery performance:

- **Deployment Frequency** — how often code is released to production
- **Lead Time for Changes** — time from commit to deployment
- **Change Failure Rate** — percentage of deployments that cause incidents
- **Time to Restore** — time to recover from a production failure

These require additional signals beyond GitHub (deployment events, incident data) and are scoped to a later phase.

---

## 7. System Architecture

EngFlow follows a **medallion-style pipeline architecture**, which organizes data into three progressive layers of quality and structure.

```
GitHub API
    ↓
Data Collector (scheduled ingestion)
    ↓
Bronze Layer — raw storage
    ↓
Silver Layer — normalized records
    ↓
Gold Layer — analytics tables
    ↓
Analytics API
    ↓
Dashboard / Query Interface
```

### 7.1 Data Collector

A scheduled service responsible for fetching repository activity from the GitHub REST API. Key responsibilities:

- Authenticates with GitHub using a personal access token or GitHub App
- Fetches commits, pull requests, reviews, and workflow runs via the REST API
- Handles pagination (GitHub returns a maximum of 100 results per page)
- Respects and recovers from GitHub API rate limits (5,000 requests/hour for authenticated requests)
- Stores raw API responses in the Bronze layer without transformation
- Runs on a configurable schedule (e.g. every 15 minutes for near-real-time data)
- Uses incremental ingestion via `since` parameters so only new events are fetched after the initial backfill

### 7.2 Bronze Layer (Raw Storage)

Raw GitHub API responses stored as received. This layer exists to preserve the original data in case processing logic changes, enable full reprocessing without re-hitting the GitHub API, maintain a complete and auditable event history, and serve as the recovery point if downstream data is corrupted.

### 7.3 Silver Layer (Processed Records)

Cleaned, normalized records derived from the Bronze layer. Responsibilities include mapping raw GitHub fields into consistent internal schemas, resolving contributor identities, computing derived fields (e.g. PR cycle time from `created_at` to `merged_at`), filtering out bots and automated merge commits, and flagging records that fail validation.

### 7.4 Gold Layer (Analytics Tables)

Aggregated, pre-computed metrics that power dashboards and API responses. The Gold layer is optimized for query speed, not raw storage. It is rebuilt from the Silver layer on a schedule.

---

## 8. Data Model

### Bronze Tables

| Table                      | Description                                                     |
| -------------------------- | --------------------------------------------------------------- |
| `raw_github_commits`       | Raw commit objects from the GitHub commits API                  |
| `raw_github_pull_requests` | Raw PR objects including state, timestamps, author              |
| `raw_github_reviews`       | Raw review events associated with pull requests                 |
| `raw_github_workflow_runs` | Raw GitHub Actions workflow run records                         |
| `raw_ingestion_log`        | Metadata about each ingestion run: timing, record count, errors |

### Silver Tables

| Table           | Description                                                        |
| --------------- | ------------------------------------------------------------------ |
| `repositories`  | Canonical repository records with metadata                         |
| `contributors`  | Normalized contributor identities, deduplication of email variants |
| `commits`       | Cleaned commit records linked to repository and contributor        |
| `pull_requests` | Normalized PR records with computed cycle time fields              |
| `reviews`       | Normalized review events linked to PR and reviewer                 |
| `workflow_runs` | Normalized CI workflow run records with outcome and duration       |

#### `commits` schema (core fields)

| Field             | Type      | Description                               |
| ----------------- | --------- | ----------------------------------------- |
| `id`              | uuid      | Internal primary key                      |
| `repository_id`   | uuid      | FK to repositories                        |
| `contributor_id`  | uuid      | FK to contributors (normalized)           |
| `commit_sha`      | text      | GitHub commit SHA                         |
| `message`         | text      | Full commit message                       |
| `committed_at`    | timestamp | Commit timestamp (author date)            |
| `is_merge_commit` | boolean   | Whether this is an automated merge commit |
| `ingested_at`     | timestamp | When EngFlow first saw this record        |

#### `pull_requests` schema (core fields)

| Field                   | Type      | Description                                      |
| ----------------------- | --------- | ------------------------------------------------ |
| `id`                    | uuid      | Internal primary key                             |
| `repository_id`         | uuid      | FK to repositories                               |
| `pr_number`             | integer   | GitHub PR number                                 |
| `author_contributor_id` | uuid      | FK to contributors                               |
| `state`                 | enum      | open, merged, closed                             |
| `created_at`            | timestamp | When the PR was opened                           |
| `first_review_at`       | timestamp | When the first review was submitted              |
| `merged_at`             | timestamp | When the PR was merged (null if not merged)      |
| `cycle_time_hours`      | float     | Computed: created_at to merged_at in hours       |
| `review_latency_hours`  | float     | Computed: created_at to first_review_at in hours |

### Gold Tables

| Table                          | Description                                                |
| ------------------------------ | ---------------------------------------------------------- |
| `daily_commit_metrics`         | Per-repo commit counts, unique contributors, by day        |
| `weekly_pr_metrics`            | PR open/merge rates, average cycle time, by week           |
| `ci_health_metrics`            | CI success rate, failure rate, average duration, by period |
| `repo_activity_summary`        | Rolling 30-day activity score per repository               |
| `contributor_activity_metrics` | Per-contributor commit and PR volume over time             |

---

## 9. Core Metrics

### Commit Metrics

| Metric                  | Description                                           |
| ----------------------- | ----------------------------------------------------- |
| Commits per day         | Total commits to a repository per calendar day        |
| Active contributors     | Unique authors who committed in the last 7 or 30 days |
| Commits per contributor | Commit volume broken down by individual author        |
| Commit velocity trend   | Week-over-week change in commit volume (% delta)      |
| First-time contributors | New authors making their first commit to the repo     |

### Pull Request Metrics

| Metric              | Description                                        |
| ------------------- | -------------------------------------------------- |
| PR open rate        | Number of new PRs opened per week                  |
| PR merge rate       | Number of PRs merged per week                      |
| Average cycle time  | Mean time from PR creation to merge, in hours      |
| Review latency      | Mean time from PR creation to first review comment |
| PR age distribution | Breakdown of open PRs by days since creation       |
| PR merge ratio      | Merged / (Merged + Closed without merge)           |

### CI Metrics

| Metric                    | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| CI success rate           | Percentage of workflow runs that completed successfully |
| CI failure rate           | Percentage of workflow runs that failed                 |
| Average workflow duration | Mean run time in minutes                                |
| Failure trend             | Week-over-week change in failure rate                   |
| Flaky workflow signal     | Runs that alternate pass/fail on the same commit SHA    |

### Repository Health Metrics

| Metric                    | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| Activity score            | Rolling composite of commits, PRs, and reviews over 30 days |
| Stagnation flag           | Repos with no commits in the last 14 days                   |
| Contributor concentration | Percentage of commits from the top 1–2 contributors         |
| Contributor growth        | New unique contributors added month-over-month              |

---

## 10. V1 Scope

### Objective

Prove the end-to-end pipeline works — from GitHub API to computed metric — using commit data only. Every downstream feature depends on this foundation being reliable.

### V1 Features

- Connect to one or more GitHub repositories using a personal access token
- Fetch full commit history (initial backfill) and new commits on a schedule
- Store raw commit data in the Bronze layer
- Normalize and process commit records into the Silver layer
- Compute daily and weekly commit metrics in the Gold layer
- Expose commit metrics through a basic REST API endpoint
- Basic dashboard or reporting view showing per-repo commit activity

### V1 Deliverables (Metrics)

- Commits per day (per repository)
- Active contributors (7-day and 30-day windows)
- Commits per contributor (ranked)
- Commit velocity trend (week-over-week)

### V1 Out of Scope

Pull request data, review data, CI/workflow data, alerts, DORA metrics, organization-level views, and contributor identity deduplication are all explicitly deferred to V2 and beyond.

### Success Criteria

V1 is successful when a user can connect a GitHub repository and see accurate, up-to-date commit metrics that match what GitHub itself reports — without any manual data handling.

---

## 11. Phased Roadmap

### Phase 1 — Foundation

- Define project scope and confirm stack decisions
- Design and provision database schema (Bronze + Silver tables)
- Set up repository structure and local development environment
- Establish coding standards and review process

### Phase 2 — Ingestion

- Implement GitHub API client with authentication and rate limit handling
- Build initial historical backfill for commits
- Store raw responses in the Bronze layer
- Add incremental ingestion (only fetch since last run)
- Implement ingestion logging and error handling

### Phase 3 — Processing

- Build transformation job: raw commits → normalized Silver records
- Handle edge cases: merge commits, bot authors, missing timestamps
- Add basic data quality checks (flag invalid records, log anomalies)

### Phase 4 — Metrics

- Build aggregation jobs: Silver commits → Gold daily metrics
- Compute V1 metrics: commits per day, active contributors, velocity trend
- Expose metrics via REST API
- Validate computed metrics against GitHub's own UI for accuracy

### Phase 5 — Presentation

- Build a basic dashboard or reporting endpoint
- Display per-repository commit activity summary
- Show contributor breakdown and velocity trend

### Phase 6 — PR Analytics (V2)

- Add pull request and review ingestion
- Compute cycle time, review latency, PR merge rate
- Surface PR metrics in the dashboard

### Phase 7 — CI Analytics (V3)

- Add GitHub Actions workflow run ingestion
- Compute CI success rate, failure trend, average duration
- Flag flaky workflow signals

### Phase 8 — Intelligence (V4)

- Add anomaly detection and configurable alerts
- Implement DORA-aligned metric calculations
- Add organization-level views across multiple repositories
- Add contributor concentration risk scoring

---

## 12. Open Technical Decisions

These should be resolved before or during Phase 1, as they affect implementation throughout.

| Decision              | Options                                    | Recommendation                                                              |
| --------------------- | ------------------------------------------ | --------------------------------------------------------------------------- |
| Programming language  | Python, TypeScript/Node, Go                | Python for data work; TypeScript if the team prefers a unified stack        |
| Database              | PostgreSQL, SQLite (dev), BigQuery, DuckDB | PostgreSQL for simplicity; DuckDB worth evaluating for analytics queries    |
| Ingestion strategy    | Polling on schedule vs GitHub webhooks     | Start with polling; webhooks are more complex and require a public endpoint |
| API framework         | FastAPI, Express, Flask                    | FastAPI (Python) or Express (Node) depending on stack choice                |
| Dashboard approach    | Build vs. embed (Metabase, Grafana)        | Embed Metabase or Grafana for V1 to avoid building a frontend               |
| GitHub authentication | Personal access token vs GitHub App        | PAT for V1 simplicity; GitHub App for multi-org scale later                 |
| Hosting               | Local only, Railway, Render, Fly.io, AWS   | Railway or Render for quick deployment without infrastructure overhead      |
| Job scheduling        | Cron, APScheduler, Celery                  | APScheduler or simple cron for V1; Celery if job complexity grows           |

---

## 13. Team Responsibilities

EngFlow is being built by two people. A clean split avoids blockers and ensures both contributors have clear ownership.

### Person 1 — Data Pipeline & Backend

- GitHub API integration and ingestion scripts
- Bronze and Silver layer schema design and migrations
- Processing and transformation jobs
- Gold layer aggregation jobs
- REST API for exposing metrics
- Ingestion scheduling, error handling, and logging

### Person 2 — Analytics & Product Surface

- Metric definitions and query logic
- Gold layer query design
- Dashboard or frontend implementation
- Reporting views and visualization
- UX for presenting insights to end users

### Shared Responsibilities

- System and data model design decisions
- Project planning and phase prioritization
- Testing strategy and validation of computed metrics
- Documentation

---

## 14. Risks and Mitigations

| Risk                                                              | Likelihood | Impact | Mitigation                                                                           |
| ----------------------------------------------------------------- | ---------- | ------ | ------------------------------------------------------------------------------------ |
| GitHub API rate limits blocking ingestion                         | Medium     | High   | Use incremental ingestion (`since` parameter), cache tokens, add exponential backoff |
| Metric definitions drifting unclear                               | High       | Medium | Define all metrics in writing before implementing queries                            |
| Overbuilding before validating the pipeline                       | High       | High   | Keep V1 strictly commit-only; defer all other data types                             |
| Bot and automated commit noise polluting metrics                  | Medium     | Medium | Add bot filtering to Silver layer processing; flag merge commits                     |
| Contributor identity fragmentation (same person, multiple emails) | Medium     | Medium | Build contributor deduplication in Silver layer — don't skip this                    |
| Trying to build a frontend too early                              | Medium     | Medium | Use an embedded tool (Metabase, Grafana) for V1 to stay focused on the pipeline      |
| Schema changes requiring full data reprocess                      | Low        | High   | Store raw Bronze layer permanently so full reprocessing is always possible           |

---

## 15. Example Product Output

### Repository Summary — `backend-api`

```
Period: Last 7 days

Commits:                    46
Active contributors:         8
Commits this week vs last:  +12% ↑
Top contributor:            @alex (14 commits)

PRs opened:                  9
PRs merged:                  8
Average merge time:         19 hours
Review latency:              4.2 hours
Open PRs > 3 days:           1

CI success rate:            91%
Avg workflow duration:       4m 12s
Failed runs this week:       4
```

### Questions EngFlow Should Answer

- Which repositories slowed down significantly this month?
- Are pull requests sitting too long before first review?
- Has CI reliability degraded in the last 14 days?
- Which repositories are active versus effectively stagnant?
- Is commit activity concentrated in one or two people?
- Are new contributors being successfully onboarded?
- Which teams are accelerating and which are stuck?

---

## 16. Why This Project Is Worth Building

EngFlow demonstrates a full-stack data engineering project with real-world applicability: API ingestion, a medallion-style data pipeline, analytics computation, and a product surface that delivers genuine value to a real user persona.

It is meaningfully more sophisticated than a dashboard project. It shows systems thinking, data modeling discipline, ETL design, and the ability to define and compute metrics from scratch — not just visualize data that already exists.

The work maps directly to roles in data engineering, backend engineering, and developer productivity tooling — areas with strong hiring demand.

**Resume framing:**

> Built EngFlow, a developer analytics platform that ingests GitHub engineering activity and computes productivity metrics including PR cycle time, CI success rate, and contributor velocity using a medallion-style data pipeline (Bronze → Silver → Gold).

---

_This document should be treated as a living spec. Decisions made during development should be reflected here as they are finalized._
