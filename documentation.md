u# EngFlow Documentation

## 1. Project Overview

**EngFlow** is a developer analytics platform that converts GitHub activity into engineering performance insights.

In simple terms, EngFlow collects events from GitHub repositories, stores them, processes them, and turns them into metrics that help engineering teams understand how work is flowing.

The product can be thought of as:

> Google Analytics for engineering teams instead of websites.

EngFlow is not a code hosting platform. GitHub remains the source of truth for engineering work. EngFlow acts as an analytics layer on top of that work.

---

## 2. Problem Statement

Engineering managers, tech leads, and founders often need answers to questions such as:

- Are developers shipping faster or slower over time?
- Are pull requests waiting too long for review or merge?
- Is CI reliable, or failing too often?
- Which repositories are active and healthy?
- Where are delivery bottlenecks forming?

Today, these questions are often answered by manually checking GitHub, exporting data, or building one-off dashboards. That process is slow, inconsistent, and difficult to scale.

EngFlow solves this by automatically collecting engineering events and computing metrics from them.

---

## 3. Product Vision

EngFlow should help teams move from raw GitHub activity to clear engineering insights.

The long-term goal is to provide a reliable system where a team can connect repositories and immediately understand:

- engineering activity
- delivery speed
- review bottlenecks
- CI health
- repo-level trends

The core idea in one sentence:

> EngFlow converts raw GitHub engineering activity into measurable signals about how software development is flowing.

---

## 4. Target Users

EngFlow is mainly intended for:

- Engineering managers
- Tech leads
- CTOs and startup founders
- Developer productivity teams

These users are usually less interested in raw events and more interested in summarized answers, trends, and bottlenecks.

---

## 5. Goals and Non-Goals

### Goals

- Collect engineering activity from GitHub
- Store raw data reliably
- Process that data into structured records
- Compute useful engineering metrics
- Expose those metrics through an API or dashboard
- Build a system that can grow from simple commit analytics into broader engineering intelligence

### Non-Goals

- Building a Git hosting platform
- Replacing GitHub
- Building a full project management tool
- Measuring developer value using simplistic vanity metrics
- Creating a production-grade enterprise analytics suite in V1

---

## 6. What EngFlow Does

EngFlow has four main responsibilities.

### 6.1 Collect Engineering Activity

The system pulls raw activity from GitHub, such as:

- commits
- pull requests
- reviews
- workflow runs / CI runs

These events represent how engineering work is happening inside a repository.

### 6.2 Store the Data

All collected data is stored in a database.

Example entities:

- repositories
- contributors
- commits
- pull_requests
- reviews
- workflow_runs

This becomes the engineering data warehouse for the product.

### 6.3 Process the Data

The raw data is cleaned, normalized, and transformed into structured records that are easier to query and analyze.

Examples:

- normalized commit records
- structured pull request records
- workflow run summaries

### 6.4 Generate Insights

The processed records are aggregated into metrics that answer real engineering questions.

Example output:

```text
Repo: backend-api

Commits this week: 46
Active contributors: 8
Average PR merge time: 19 hours
CI success rate: 91%
```

---

## 7. System Architecture

EngFlow follows a pipeline-based architecture:

```text
GitHub API
    ↓
Data Collector
    ↓
Raw Data Storage
    ↓
Processing Jobs
    ↓
Analytics API
    ↓
Dashboard / Queries
```

### 7.1 Data Collector

A service or script that fetches repository activity from the GitHub API.

Examples:

- `GET /repos/{owner}/{repo}/commits`
- `GET /repos/{owner}/{repo}/pulls`
- `GET /repos/{owner}/{repo}/actions/runs`

Responsibilities:

- authenticate with GitHub
- fetch repository event data
- handle pagination and rate limits
- ingest data on a schedule

### 7.2 Raw Storage

This is the Bronze layer in a medallion-style architecture.

Purpose:

- preserve original GitHub responses
- support reprocessing if logic changes
- maintain an auditable raw event history

### 7.3 Processed Storage

This is the Silver layer.

Purpose:

- clean and normalize raw records
- map fields into consistent schemas
- prepare data for analytics queries

### 7.4 Analytics Layer

This is the Gold layer.

Purpose:

- calculate aggregate metrics
- support dashboards and reporting
- make trends easy to query

---

## 8. Data Model

The exact schema may evolve, but the initial design should include the following core tables.

### Raw Tables

- `raw_github_events`
- `raw_commits`
- `raw_pull_requests`
- `raw_reviews`
- `raw_workflow_runs`

### Structured Tables

- `repositories`
- `contributors`
- `commits`
- `pull_requests`
- `reviews`
- `workflow_runs`

### Analytics Tables

- `daily_commit_metrics`
- `repo_activity_metrics`
- `pr_performance_metrics`
- `ci_health_metrics`

Example fields for a `commits` table:

- `id`
- `repository_id`
- `author_name`
- `author_email`
- `commit_sha`
- `message`
- `committed_at`

Example fields for a `pull_requests` table:

- `id`
- `repository_id`
- `pr_number`
- `author`
- `state`
- `created_at`
- `merged_at`
- `closed_at`

---

## 9. Core Metrics

These metrics make EngFlow feel like a real analytics product instead of a basic GitHub viewer.

### Commit Metrics

- commits per day
- commits per contributor
- active contributors
- commit trend over time

### Pull Request Metrics

- PRs opened
- PRs merged
- average PR merge time
- review latency
- open PR aging

### CI Metrics

- CI success rate
- CI failure rate
- average workflow duration
- failed workflow trend

### Repo Health Metrics

- activity by repository
- inactive or stagnant repositories
- contributor concentration

---

## 10. V1 Scope

Version 1 should remain intentionally small.

### V1 Objective

Prove the pipeline works end to end by using commit data only.

### V1 Features

- connect to a GitHub repository
- fetch commit data
- store commit data
- process and normalize commit records
- compute simple commit metrics
- display results through a basic API or dashboard

### V1 Metrics

- commits per day
- commits per contributor
- active contributors
- commit activity trend

### Why This Scope

This is enough to validate:

- GitHub ingestion
- storage design
- transformation logic
- analytics computation
- basic product usefulness

Everything else, such as PR and CI metrics, can be added after the pipeline is stable.

---

## 11. Future Scope

After V1, EngFlow can expand in phases.

### V2

- pull request ingestion
- review analytics
- PR merge time
- open vs merged PR reporting

### V3

- GitHub Actions / CI workflow analytics
- CI success and failure trends
- average workflow duration

### V4

- DORA-aligned indicators
- multi-repo organization views
- alerts for bottlenecks or sudden regressions

---

## 12. Example Product Output

### Engineering Overview

```text
Commits (7 days): 82
Active Contributors: 12
PRs Opened: 19
PRs Merged: 17
Average Merge Time: 21 hours
CI Success Rate: 93%
```

### Example Questions EngFlow Should Answer

- Which repositories slowed down this month?
- Are pull requests sitting too long before merge?
- Has CI reliability dropped this week?
- Which repositories are active versus stagnant?
- How many contributors were active in the last 7 days?

---

## 13. Technical Learning Value

EngFlow is a strong technical project because it demonstrates:

- API ingestion
- backend system design
- data modeling
- ETL / ELT pipeline thinking
- analytics computation
- repository-level metrics design

This is more than a dashboard project. It shows systems thinking and data engineering fundamentals.

Resume summary example:

> Built EngFlow, a developer analytics platform that ingests GitHub engineering activity and computes productivity metrics using a medallion-style data pipeline.

---

## 14. Team Working Model

Since this project is being built by two people, responsibilities should be clearly divided.

### Suggested Split

**Person 1: Data Pipeline / Backend**

- GitHub API integration
- data ingestion scripts or services
- database schema design
- processing jobs
- analytics API

**Person 2: Analytics / Product Surface**

- metric definitions
- query logic
- dashboard or frontend
- reporting views
- UX for presenting insights

Both contributors should collaborate on:

- system design
- project planning
- data model decisions
- testing
- documentation

---

## 15. Development Phases

### Phase 1: Foundation

- define project scope
- choose stack
- create database schema
- set up repository structure

### Phase 2: Ingestion

- connect to GitHub API
- fetch commit data
- store raw records

### Phase 3: Processing

- normalize commit records
- build transformation jobs
- create analytics tables

### Phase 4: Metrics

- compute commit metrics
- expose metrics via API
- validate results against GitHub

### Phase 5: Presentation

- build a basic dashboard or reporting endpoint
- show repo-level insights

### Phase 6: Expansion

- add PR analytics
- add CI analytics
- add trend analysis and alerts

---

## 16. Open Decisions

The following decisions should be finalized early:

- programming language and framework
- database choice
- ingestion strategy: polling vs scheduled jobs
- dashboard vs API-first delivery
- hosting and deployment approach
- authentication and GitHub token management

These decisions affect implementation speed and project complexity.

---

## 17. Risks

Potential project risks:

- GitHub API rate limits
- unclear metric definitions
- overbuilding too early
- collecting too much raw data before defining useful outputs
- trying to support commits, PRs, reviews, and CI all at once in V1

To reduce risk:

- keep V1 focused on commits only
- define metrics before implementing dashboards
- store raw data so processing can be improved later
- validate metrics with small real examples

---

## 18. Summary

EngFlow is a developer analytics platform built on top of GitHub activity.

It collects engineering events, stores them in a structured pipeline, processes them into metrics, and presents insights about engineering flow.

The first version should focus only on commit ingestion and basic commit analytics. Once that pipeline is reliable, the project can expand into pull request metrics, CI insights, and broader engineering health reporting.
