# Three-minute demo walkthrough

This is a script for a local demonstration, not a claim that a video has been recorded or the service deployed.

1. **Problem (0:00–0:30):** Show the fictional brief. The support specialist needs applicable guidance and control over the reply.
2. **Normal path (0:30–1:25):** Start the FastAPI server from README. In `/docs`, submit `My VPN connection fails every morning`. Show the category, `KB-NETWORK-01` evidence ID, source-linked draft and pending review. Approve an edited response through the review endpoint. Explain that no message is sent.
3. **Failure path (1:25–2:15):** Submit `My password was leaked`. Show `sensitive=true`, no retrieved evidence, `needs_escalation=true`, and the review interrupt. Reject the draft. Explain why a generic recovery article would be inappropriate.
4. **Evidence and next step (2:15–3:00):** Run the two retrieval evaluation commands, `python -m evals.run_product_eval` with model variables unset, and the test suite. Open `TEST_REPORT.md`, describe the original nine false matches and the two challenge-set security misses that led to changes. State that real ticket performance, persistence, authentication and costs still need assessment.
