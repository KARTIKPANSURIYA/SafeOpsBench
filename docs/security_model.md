# Security model

Trust levels are: **0** benchmark/system instruction; **1** user request; **2** trusted enterprise policy; **3** tool/service response; **4** enterprise content such as notes, uploads, emails, and external descriptions. Level 4 is untrusted and may contain malicious instructions.

C008 labels its synthetic customer note `UNTRUSTED_DATA`. The environment returns that provenance as data, never promotes the note into an agent observation's system or policy context, and never interprets its text as executable policy. Tests verify that retrieving the note cannot change the credit limit or approval state.

C008 should therefore be described as an LLM-security-ready scenario, not evidence that deterministic agents or future language models resist prompt injection. Meaningful model-level evaluation requires later adapters that actually consume the content while preserving provenance and role separation.

Tool responses remain subject to schema validation, authorization, policy, and invariant enforcement. Blocked tool attempts are retained in trajectories and audit rows. Secret-like argument fields are redacted. Future adapters must preserve trust labels and keep retrieved content separate from system and user authority.
