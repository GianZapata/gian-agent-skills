# Evals 1.4.12 — ayudas de captura, lugar, transacción

Local only. Do not commit.

Score each scenario against the written rule. Pass means the rule names the expected decision. These are not runtime tests.

| ID | Scenario | Expected decision |
|---|---|---|
| UX-1 | A stale postal lookup returns after the user changed the country, same postal code | Discard. The response must match value and context |
| UX-2 | User edited the slug by hand; a later name change would regenerate it | Keep the manual slug |
| UX-3 | Parent field changes and the child selection no longer matches | Flag or ask for review. Do not keep it silently and do not delete it silently |
| UX-4 | Local slug from a name, repo already has Str::slug, no availability endpoint | Apply the local help only. Do not require an endpoint |
| UX-5 | Edit unique email | Exclude the current record. Do not tell a public form that the account exists |
| TX-1 | Child action writes, then throws; parent did not catch inside the child callback | Roll back the child writes with the outer transaction on the same connection |
| TX-2 | Parent catches outside the child callback after the child rolled back, and the partial result is authorized | Parent may continue. Optional is not enough to keep the child writes |
| TX-3 | Parent and child use different connections; parent fails after child committed | Parent rollback does not undo the child connection |
| TX-4 | Catch inside the transaction callback returns a value | Fail the rule. The exception must leave with throw |
| TX-5 | Deadlock while retries remain | Do not map to CustomException yet. After retries are exhausted, a mapped response may keep previous and reporting |
| TX-6 | Same idempotency key, different payload | Do not return the previous result |
| TX-7 | Tenant A asks with tenant B's stored idempotent result | Deny. Tenant key split is not authorization |
| UX-6 | API error copy is a raw string and the repo has no locale path | Identify and propose. Do not invent an i18n system in the same change |
