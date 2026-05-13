# Challenge 4: Production Workflow

Build a multi-agent orchestration workflow for TireForge Industries and take it to production.

## Scenario

The individual agents you built in Challenge 1 are valuable — but in production, agents need to work
**together** as an automated pipeline. In this challenge you wire the two agents into a full
factory health workflow that runs automatically and produces a structured report.

## Learning Objectives

- Deploy persistent production agents (create once, reuse forever)
- Orchestrate multiple agents step-by-step in a workflow
- Handle agent-to-agent data flow (pass anomaly results into the diagnosis step)
- Generate a consolidated factory health report

## The Workflow

```
ensure_agents_deployed()
        |
        v
run_anomaly_scan()          <-- Anomaly Detection Agent checks all 5 machines
        |
        v (for each machine with anomalies)
run_fault_diagnosis()       <-- Fault Diagnosis Agent diagnoses root cause
        |
        v
print_factory_report()      <-- Consolidated Health Report
```

## Tracks

| Track | Description |
|-------|-------------|
| [Portal Track](./portal-track/README.md) | Use Foundry portal to explore the deployed agents and test the workflow |
| [SDK Track](./sdk-track/README.md) | Build the full workflow in Python using the Azure AI Projects SDK |

## Success Criteria

- Both agents are listed in the Foundry portal as persistent assets
- The workflow runs from end-to-end: anomaly scan -> diagnosis -> report
- The factory health report correctly identifies anomalous machines and their diagnoses
- Re-running the script reuses existing agents (no duplicate creation)
