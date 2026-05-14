# Challenge 0: Setup & Authentication

## Objectives

By the end of this challenge, you will have:
- ✅ A fully provisioned Azure AI Foundry project with a deployed model
- ✅ Application Insights provisioned and connection string available
- ✅ Verified authentication from your local machine to Foundry
- ✅ Confirmed your agent endpoint is working

## Time: ~15 minutes

## Before You Start

Make sure you've already run `deploy.sh` — if you haven't, do it now!

```bash
bash challenge-0-setup/deploy.sh
```

This will provision all resources **and** automatically write your `.env` file to the repository root as `.env`.

## Get Started

Run the setup verification:

```bash
cd challenge-0-setup
python verify_setup.py
```

See [solutions/verify_setup.py](./solutions/verify_setup.py) if you get stuck.

## Success Criteria

- [ ] You can see your AI Foundry project in the Azure Portal
- [ ] A model deployment for gpt-5.1 or gpt-5.4 shows "Succeeded" status
- [ ] You can either: send a test message in the Foundry Playground (Portal) or run `verify_setup.py` without errors (SDK)
