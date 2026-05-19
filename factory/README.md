# 🏭 Scenario: Predictive Maintenance — TireForge Industries

## Background

**TireForge Industries** operates a tire manufacturing plant with 5 critical machines:

- **MX-001** (Mixer) — Blends raw rubber compounds
- **EX-002** (Extruder) — Shapes rubber into tire tread profiles
- **CP-003** (Curing Press) — Vulcanizes tires under heat and pressure
- **CU-004** (Cooling Unit) — Gradually cools cured tires
- **IS-005** (Inspection Station) — Quality assurance via vibration analysis

Each machine emits real-time sensor data: temperature, pressure, vibration, and RPM.

## Your Mission

Build an AI agent system that:

1. **Detects anomalies** — Compares sensor readings against thresholds
2. **Diagnoses faults** — Reasons about root causes from anomaly patterns
3. **Reports health** — Produces a consolidated factory health report

## Challenges

| # | Challenge | What You'll Do | Time |
|---|-----------|---------------|------|
| 0 | [Setup](./challenge-0-setup/README.md) | Deploy Microsoft Foundry infrastructure | 20 min |
| 1 | [Build Agents](./challenge-1-build/README.md) | Create Anomaly Detection + Fault Diagnosis agents | 35 min |
| 2 | [Monitor](./challenge-2-monitor/README.md) | Enable GenAI tracing with Application Insights | 20 min |
| 3 | [Evaluate](./challenge-3-evaluate/README.md) | Run systematic quality evaluations | 25 min |
| 4 | [Production Workflow](./challenge-4-deploy/README.md) | Multi-agent orchestration + portal workflow | 20 min |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Microsoft Foundry                       │
│                                                         │
│  ┌─────────────────┐      ┌──────────────────────┐     │
│  │ Anomaly Agent   │      │  Fault Diagnosis     │     │
│  │ (+ tool:        │─────▶│  Agent               │     │
│  │  check_thresh.) │      │                      │     │
│  └────────┬────────┘      └──────────┬───────────┘     │
│           │                          │                  │
│           ▼                          ▼                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Factory Health Workflow                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────┐  │
│  │ App Insights │  │  Evaluation   │  │  Tracing   │  │
│  └──────────────┘  └───────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────┘
```
