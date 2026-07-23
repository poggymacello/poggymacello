### Poggy Macello

Cybersecurity / ML portfolio. Six projects, one gone deep (real dataset, leakage-safe evaluation, deployed inference service), five kept honest about being synthetic demonstrations.

| Project | What it does | Method | Data | Link |
|---|---|---|---|---|
| **shadowtrace** | Network traffic anomaly detection, deployed as an API | Gaussian HMM vs. Isolation Forest vs. logistic regression | **Real** (UNSW-NB15) | [repo](https://github.com/poggymacello/shadowtrace) |
| phishnet-ai | Phishing email classification | Attention-based NN vs. TF-IDF baseline | Synthetic | [repo](https://github.com/poggymacello/phishnet-ai) |
| electroshield | Smart-grid IoT anomaly detection | Isolation Forest vs. statistical control chart | Synthetic | [repo](https://github.com/poggymacello/electroshield) |
| iotlock | IoT network resilience simulation | Scale-free topology, centrality analysis, mitigation strategies | Synthetic | [repo](https://github.com/poggymacello/iotlock) |
| malwaremorph | Entropy-based packed/encrypted-content detection | Logistic regression vs. entropy-threshold baseline | Synthetic | [repo](https://github.com/poggymacello/malwaremorph) |
| cryptosentry | RSA + classical-vs-quantum factoring cost | Real bignum RSA, cited complexity comparison | N/A (generated keys, no dataset) | [repo](https://github.com/poggymacello/cryptosentry) |

**shadowtrace** is the one to look at first: a real, labeled IDS dataset (UNSW-NB15), an explicit leakage audit (temporal split, single-feature AUC checks, cross-split duplicate detection), three models evaluated honestly against each other (including where the project's own namesake method loses), and a FastAPI service with a versioned model artifact, Docker deployment, a measured latency benchmark, and an incremental streaming scorer.

The other five are intentionally lighter: synthetic data, clearly labeled as such, used to demonstrate a specific technique (attention mechanisms, anomaly detection baselines, network resilience simulation, entropy-based detection, RSA internals) without overclaiming real-world performance. Every repo says so at the top of its own README.
