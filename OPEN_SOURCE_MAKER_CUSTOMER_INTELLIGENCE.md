# Advait Open-Source Maker & Customer Intelligence

## Mission
Discover open-source projects, understand from repository metadata and README evidence what they were built to do, identify their makers/maintainers, and map plausible tool capabilities to verified customer needs. This creates two relationship paths: customers who need work/services, and makers/maintainers whose tools may help those customers.

## What the module analyzes
- Repository owner/name, description, topics, README excerpt, declared SPDX license, stars/forks, issue count, last update, releases, and source URLs.
- Tool purpose taxonomy: automation, developer tools, data/analytics, AI/ML, design/content, business operations, security/privacy, education/knowledge, and communication.
- Maintenance and missing-evidence signals.
- Potential matches between tool purpose and customer need.
- Frequency of tool categories and maker-to-customer match candidates.

## What it does not claim
- A repository owner is not automatically the original creator or an authorized commercial contact.
- Stars/forks do not prove quality, security, support, or suitability.
- README text is the project's stated purpose, not independent proof.
- A missing license means usage rights are not confirmed; do not assume permission.
- A potential match is not a validated solution.
- This module does not crawl, message maintainers, contact customers, install software, run code, negotiate, or deploy tools.

## Defense gates before recommending a tool
1. Confirm source repository and current maintainer identity through official project channels.
2. Read the actual license and confirm permitted use, modification, redistribution, and commercial terms.
3. Review maintenance, releases, dependency health, security policy, vulnerabilities, and build/release practices.
4. Review data collection, telemetry, permissions, network access, and privacy implications.
5. Test compatibility in an isolated environment before customer use.
6. Obtain owner approval before any external contact, recommendation sent on the owner's behalf, integration, or paid commitment.

OpenSSF Scorecard is a useful external security signal, not a guarantee or substitute for review. It scores individual repository security practices and explicitly warns that aggregate scores can hide differing check-level behavior. Reference: https://scorecard.dev/ and https://github.com/ossf/scorecard.

## Run tests
```sh
python -m unittest -v tests.test_open_source_intelligence
```

## Integration status
The module accepts project and customer-need records supplied by a separate authorized collector. It is offline analysis only. Live GitHub discovery, README retrieval, Scorecard/OSV enrichment, a persistent evidence store, and a continuously running feed are separate pending integrations.
