# Challenge 2: Deploy & Expose via API Management

## Objectives

By the end of this challenge, you will have:
- ✅ Versioned your agents for production use
- ✅ Exposed your Foundry model endpoint through Azure API Management
- ✅ Configured AI Gateway policies (rate limiting, authentication)
- ✅ Verified the APIM gateway responds correctly

## Time: ~30 minutes

## Context

Your agents work locally — but in production, you don't expose AI endpoints directly to consumers. Azure API Management acts as a gateway layer providing:

- **Rate limiting** — Prevent abuse and control costs
- **Authentication** — Subscription keys, OAuth, managed identity
- **Monitoring** — Request/response logging, analytics
- **Caching** — Semantic caching for repeated queries
- **Load balancing** — Distribute across multiple backends

## Prerequisites

- APIM should be in "Succeeded" state. Check:
  ```bash
  az apim show --name <your-apim-name> --resource-group foundry-hackathon-rg --query provisioningState
  ```
- If still "Activating", ask your facilitator for the shared APIM instance

## Choose Your Track

| Track | Go to |
|-------|-------|
| Portal Track | [portal-track/README.md](./portal-track/README.md) |
| SDK Track | [sdk-track/README.md](./sdk-track/README.md) |

## Success Criteria

- [ ] APIM gateway URL returns a valid response when called with a subscription key
- [ ] You can call the Foundry model through APIM instead of directly
- [ ] Rate limiting policy is active (hitting the endpoint rapidly should return 429)
