---
name: demo-standup
description: Generate today's standup update for the user. Trigger this when the user asks for their daily standup, update, "what should I say in standup", or wants help drafting a status post.
---

Generate the daily standup by dynamically injecting data into the `assets/standup-template.md` asset:

1. **Date**: Automatically determine the current date and format it as `YYYY-MM-DD` for the `{date}` placeholder.
2. **Yesterday**: 
   - Check the current day of the week. If today is Monday, look back `3 days ago`. Otherwise, look back `1 day ago`.
   - Run: `git log --since="<calculated_days> ago" --no-merges --pretty=format:"- %s" --author="$(git config user.email)"`
   - If the log is empty, prompt the user: "I couldn't find any recent commits. What did you work on yesterday?"
3. **Today**: Ask the user: "What are your main focus areas for today?"
4. **Blockers**: Ask the user: "Any blockers in your way?" If they say "none" or "no", populate the placeholder with `- None`.

**Output Rule**: Render the fully populated template directly in your final chat response. Do not write or save the file to disk unless explicitly requested.
