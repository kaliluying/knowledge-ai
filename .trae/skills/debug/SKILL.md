---
name: "debug"
description: "Debugs code issues by analyzing errors, adding log statements, and verifying fixes. Invoke when user encounters bugs, errors, or asks to debug issues."
---

# Debug Skill

This skill helps debug code issues through a systematic process of analysis, logging, and verification.

## Activation Trigger

The skill activates when user input contains keywords like:
- "错误" / "error" / "bug"
- "debug" / "调试"
- "问题" / "issue" / "problem"
- Exception messages or error traces

## Workflow

### Phase 1: Error Information Collection

When activated, ask user to provide:

1. **Error Description**: Detailed description of what happened
2. **Error Messages**: Full error text, stack traces, or exception messages
3. **Steps to Reproduce**: Exact steps that led to the error
4. **Relevant Code**: Code snippets related to the error
5. **Environment**: What the user is running (command, browser, etc.)

### Phase 2: Code Analysis

1. **Initial Analysis**:
   - Analyze the provided code and error message
   - Identify potential root causes
   - Locate key points in code (variable assignments, conditions, function calls)

2. **Insert Logging**:
   - Add detailed print/log statements at key points
   - Log variable values at critical moments
   - Output to a dedicated log file: `.debug/logs/debug_{timestamp}.log`

3. **Log Format**:
   ```python
   # Python example
   import logging
   import os
   from datetime import datetime

   DEBUG_LOG_DIR = Path(".debug/logs")
   DEBUG_LOG_DIR.mkdir(parents=True, exist_ok=True)

   def get_debug_log_file():
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       return DEBUG_LOG_DIR / f"debug_{timestamp}.log"

   # Usage
   logging.basicConfig(filename=str(get_debug_log_file()), level=logging.DEBUG)
   ```

### Phase 3: Reproduction & Verification

1. **Ask User to Reproduce**:
   - Request user to perform the steps that trigger the bug
   - Wait for confirmation that bug is reproduced

2. **Read and Analyze Logs**:
   - Read the generated log file
   - Verify hypothesis about root cause
   - Identify exact failure point

### Phase 4: Fix & Verify

1. **If Hypothesis Correct**:
   - Provide specific code fix
   - Ask user to reproduce again
   - Verify the fix works

2. **If Hypothesis Wrong**:
   - Add logs at new locations
   - Repeat analysis process
   - Continue until root cause found

### Phase 5: Cleanup

1. **Success**:
   - Delete all inserted log statements
   - Delete all generated log files in `.debug/logs/`
   - Confirm with user that issue is resolved

2. **Failure**:
   - Keep logs for further analysis
   - Move to new analysis points
   - Repeat process

## Log File Management

- **Location**: `.debug/logs/`
- **Naming**: `debug_{timestamp}.log`
- **Cleanup**: Always clean up after fix is verified

## Example Dialogue

```
System: I've detected a potential bug. To help debug effectively, please provide:
1. The exact error message or exception
2. Steps to reproduce
3. Any relevant code snippets

User: [Provides information]

System: Based on the analysis, I'll add logging at key points in the code. Let me create the debug setup...

[Adds logs]

System: Please reproduce the bug now. After you do, I'll analyze the logs to find the root cause.

User: [Reproduces bug]

System: [Reads logs] The logs show X is causing the issue. Here's the fix...

[Provides fix]

System: Please verify the fix by reproducing the bug again.

User: [Verifies fix works]

System: Great! I'll now clean up all the debug logs and inserted statements.
```

## Safety Requirements

- Never commit debug logs to version control
- Always clean up temporary files after debugging
- Ensure no debug code remains in production
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
