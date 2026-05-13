# Challenge 0: Setup & Authentication

## Objectives

By the end of this challenge, you will have:
- ✅ A fully provisioned Azure AI Foundry project with a deployed model
- ✅ Application Insights and API Management resources provisioned
- ✅ Verified authentication from your local machine to Foundry
- ✅ Confirmed your agent endpoint is working

## Time: ~20 minutes

## Before You Start

Make sure you've already run `deploy.sh` — if you haven't, do it now! APIM takes ~30 minutes to provision, so starting early is important.

```bash
bash challenge-0-setup/deploy.sh
```

This will provision all resources **and** automatically write your `.env` file to `challenge-0-setup/.env`.

## Choose Your Track

| Track | Go to |
|-------|-------|
| Portal Track | [portal-track/README.md](./portal-track/README.md) |
| SDK Track | [sdk-track/README.md](./sdk-track/README.md) |

## Success Criteria

- [ ] You can see your AI Foundry project in the Azure Portal
- [ ] The gpt-5.1 model deployment shows "Succeeded" status
- [ ] You can either: send a test message in the Foundry Playground (Portal) or run `verify_setup.py` without errors (SDK)
