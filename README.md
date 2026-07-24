### Poggy Macello

Cybersecurity / ML portfolio. Six projects, all now built on real, public datasets with a leakage-safe evaluation and a deployed inference service; each README documents what changed when the project moved from a synthetic demonstration to real data, including where metrics dropped and why.

| Project | What it does | Method | Data | Deployment | Link |
|---|---|---|---|---|---|
| shadowtrace | Network traffic anomaly detection | Gaussian HMM vs. Isolation Forest vs. logistic regression | Real (UNSW-NB15) | FastAPI, Docker, streaming scorer | [repo](https://github.com/poggymacello/shadowtrace) |
| phishnet-ai | Phishing URL detection | Attention NN vs. TF-IDF vs. gradient boosting | Real (PhiUSIIL) | FastAPI, Docker | [repo](https://github.com/poggymacello/phishnet-ai) |
| electroshield | Electricity theft detection | Isolation Forest vs. statistical control chart | Real (SGCC) | FastAPI, Docker | [repo](https://github.com/poggymacello/electroshield) |
| malwaremorph | Malware detection from static PE features | Entropy threshold vs. logistic regression vs. gradient boosting | Real (BODMAS/EMBER features only, never binaries) | FastAPI, Docker | [repo](https://github.com/poggymacello/malwaremorph) |
| iotlock | IoT network resilience + botnet detection | Mitigation Monte Carlo across real topologies; gradient boosting detector | Real (Internet Topology Zoo + N-BaIoT) | FastAPI, Docker, interactive dashboard | [repo](https://github.com/poggymacello/iotlock) |
| cryptosentry | RSA internals, key-risk assessment, PQC readiness | Real bignum RSA (CSPRNG keygen); NIST-guidance risk rules | Real (Certificate Transparency key survey) | FastAPI, Docker | [repo](https://github.com/poggymacello/cryptosentry) |

Every repo follows the same discipline: a manual leakage audit (not just an automated check — every suspicious signal is investigated and the reasoning is written down), a domain-appropriate split (temporal, grouped-by-domain, or device-holdout, whichever prevents the realistic leakage risk for that data), honest reporting when real-data metrics collapse relative to the earlier synthetic version (a drop is treated as the expected, correct outcome of testing against reality, not a bug), and a containerized FastAPI service actually built, run, and curl-verified end to end — not just written.

Each project's README has a "What changed from v1" section covering the exact same repo before it used real data, for anyone who wants to see the delta directly.
