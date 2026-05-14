# Challenge 1: Build Agents

## Objectives

By the end of this challenge, you will have:
- ✅ An **Anomaly Detection Agent** that monitors sensor data and flags abnormal readings
- ✅ A **Fault Diagnosis Agent** that analyzes flagged anomalies and recommends maintenance actions
- ✅ Both agents tested against real sensor data from the factory floor

## Time: ~20 minutes

## Context

TireForge Industries has 5 machines on the production floor. Each machine emits sensor data including temperature, pressure, vibration, and RPM. Your agents need to:

1. **Anomaly Detection**: Compare current readings against known thresholds and flag machines that are out of spec
2. **Fault Diagnosis**: Given an anomaly, reason about what might be wrong and recommend an action

Check out [sensor_data.json](./sensor_data.json) to see the current state of all machines.

## Get Started

Open [agents.py](./agents.py) and review the implementation of both agents.

```bash
cd factory/challenge-1-build
python agents.py
```

## Success Criteria

- [ ] Anomaly Detection Agent correctly identifies the 2 warning + 1 critical machine
- [ ] Fault Diagnosis Agent provides reasonable maintenance recommendations
- [ ] Both agents respond coherently when given a machine's sensor readings
