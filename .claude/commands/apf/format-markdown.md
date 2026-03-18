---
source: Agentic Programming Framework: https://github.com/iddolev/apf 
author: Iddo Lev for 
description: Running the markdown formatting script
last_update: 2026-03-18
---

Run the markdown formatting script.

```
python .claude/scripts/apf/format_markdown.py $ARGUMENTS
```

If `$ARGUMENTS` is empty, this runs on all markdown files (excluding sandbox/ and tmp/).
Otherwise it runs on the specified file(s) or directory.
