---
name: demo-showcase-fields
description: Explain every standard Agent Skill frontmatter field — name, description, license, compatibility, metadata, allowed-tools — using this skill's own frontmatter as a worked example. Use when the user asks to see "all the frontmatter fields", "the frontmatter demo", or to explain what each field does in a SKILL.md file.
license: MIT
compatibility: Designed for Claude Code (or similar products)
metadata:
  author: "Times of Agents"
  version: "1.0.0"
  tags: [reference, frontmatter, documentation]
allowed-tools:
  - Read
---

# Frontmatter Field Showcase

When this skill is activated, walk the user through this skill's own frontmatter from top to bottom:

1. **`name`** — The identifier; must match the parent directory name per the spec.
2. **`description`** — The trigger; what the agent reads to decide whether to load the skill.
3. **`license`** *(optional)* — The license name or reference (e.g., MIT).
4. **`compatibility`** *(optional)* — Environment notes (e.g., "Designed for Claude Code").
5. **`metadata`** *(optional)* — Arbitrary key/value bag containing details like author, version, and tags.
6. **`allowed-tools`** *(experimental)* — Tools pre-approved for use without per-use permission prompts (e.g., `Read`).

### Summary
Close the explanation by stating: "Only `name` and `description` are required. The other four fields are situational."
