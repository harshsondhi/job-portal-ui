---
name: demo-roll-dice
description: Roll dice using a random number generator. Use when asked to roll a die (d4, d6, d20, d100, etc.), roll dice, or generate a random dice roll. The course's canonical quickstart skill.
---

## Single die

Run this command, substituting the actual number of sides for `<SIDES>`:

```bash
python3 -c "import random; print(random.randint(1, <SIDES>))"
```

Examples:

- d6 → `random.randint(1, 6)`
- d20 → `random.randint(1, 20)`
- d100 → `random.randint(1, 100)`

## Multiple dice

For a roll like "3d6", run the command once per die and collect the results:

```bash
python -c "import random; results = [random.randint(1, 6) for _ in range(3)]; print('Rolls:', results, '| Total:', sum(results))"
```

Adjust the die size and count to match the request.

## Reporting results

Always show:

- Each individual roll
- The total (for multi-die rolls)
- Any modifier applied (e.g., "+2" added after rolling)
