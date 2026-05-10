"""
CCA-F Domain 4, Exercise 4 — Message Batches API (Subdomain 4.5)
=================================================================

WHAT THIS EXERCISES:
  The Message Batches API is for latency-tolerant, non-blocking work.
  It saves 50% on costs but provides no guaranteed latency SLA (up to 24h).
  It is NOT for CI pipelines, pre-merge checks, or any blocking workflow.

KEY RULES:
  - 50% cost savings vs. real-time API
  - Up to 24-hour processing window; no guaranteed latency SLA
  - Use custom_id to correlate request with response (results may be out of order)
  - For failures: resubmit ONLY failed items using their custom_id
  - Refine prompts on a SAMPLE SET before submitting large batches
  - Does NOT support multi-turn tool calling within a single request

WHEN TO USE vs. NOT USE:
  USE:     overnight reports, weekly audits, nightly test generation, batch extraction
  NOT USE: pre-merge checks, CI blocking steps, any workflow waiting on results

STRUCTURE:
  Part A -- Submit a batch (5 requests)
  Part B -- Poll for completion and retrieve results
  Part C -- Handle failures: resubmit only failed items
  Part D -- Decision framework: batch vs. real-time
"""

import sys
import time
import json

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"


# =====================================================================
# BATCH REQUESTS
# =====================================================================
# Each request has a custom_id you define.
# This is how you correlate results back to the original request.
# Results may come back in ANY ORDER -- always look up by custom_id.

BATCH_REQUESTS = [
    {
        "custom_id": "review-001",
        "params": {
            "model": MODEL,
            "max_tokens": 150,
            "messages": [
                {"role": "user", "content": "List 2 Python code review best practices. Brief bullet points only."}
            ]
        }
    },
    {
        "custom_id": "review-002",
        "params": {
            "model": MODEL,
            "max_tokens": 150,
            "messages": [
                {"role": "user", "content": "List 2 SQL security best practices. Brief bullet points only."}
            ]
        }
    },
    {
        "custom_id": "review-003",
        "params": {
            "model": MODEL,
            "max_tokens": 150,
            "messages": [
                {"role": "user", "content": "List 2 API design best practices. Brief bullet points only."}
            ]
        }
    },
    {
        "custom_id": "review-004",
        "params": {
            "model": MODEL,
            "max_tokens": 150,
            "messages": [
                {"role": "user", "content": "List 2 error handling best practices. Brief bullet points only."}
            ]
        }
    },
    {
        "custom_id": "review-005",
        "params": {
            "model": MODEL,
            "max_tokens": 150,
            "messages": [
                {"role": "user", "content": "List 2 logging best practices. Brief bullet points only."}
            ]
        }
    },
]


# =====================================================================
# PART A: SUBMIT THE BATCH
# =====================================================================

def submit_batch():
    """
    Submits all 5 requests as a single batch.
    Returns the batch object with a batch_id.
    """
    print("\n--- PART A: Submitting Batch ---")
    print(f"Submitting {len(BATCH_REQUESTS)} requests as a single batch...")
    print("NOTE: In production, refine your prompt on a sample set BEFORE submitting at scale.")
    print("      Failed batches at 10,000 requests cost more to resubmit than to test upfront.\n")

    batch = client.messages.batches.create(requests=BATCH_REQUESTS)

    print(f"Batch ID     : {batch.id}")
    print(f"Status       : {batch.processing_status}")
    print(f"Request count: {batch.request_counts.processing + batch.request_counts.succeeded + batch.request_counts.errored + batch.request_counts.canceled + batch.request_counts.expired}")
    print("""
KEY POINTS:
  - Each request has a custom_id YOU define
  - The batch ID lets you poll for status
  - Processing can take up to 24 hours (no SLA guarantee)
  - This is why batch = latency-tolerant only (never for CI checks)
""")
    return batch.id


# =====================================================================
# PART B: POLL FOR COMPLETION AND RETRIEVE RESULTS
# =====================================================================

def wait_for_batch(batch_id: str, max_wait_seconds: int = 120) -> bool:
    """
    Polls for batch completion. Returns True if completed successfully.
    In production: you'd check back after hours, not seconds.
    For this exercise: small batch, should complete quickly.
    """
    print(f"\n--- PART B: Waiting for Batch {batch_id} ---")
    print(f"Polling every 5 seconds (max {max_wait_seconds}s for this exercise)...")
    print("In production, you would check back after hours, not loop like this.\n")

    elapsed = 0
    while elapsed < max_wait_seconds:
        batch = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status
        counts = batch.request_counts

        print(f"  [{elapsed:3d}s] Status={status} | "
              f"processing={counts.processing} "
              f"succeeded={counts.succeeded} "
              f"errored={counts.errored}")

        if status == "ended":
            print(f"\nBatch completed:")
            print(f"  Succeeded: {counts.succeeded}")
            print(f"  Errored  : {counts.errored}")
            print(f"  Canceled : {counts.canceled}")
            print(f"  Expired  : {counts.expired}")
            return True

        time.sleep(5)
        elapsed += 5

    print(f"\nBatch did not complete within {max_wait_seconds}s.")
    print("This is normal for large batches -- they can take up to 24 hours.")
    return False


def retrieve_results(batch_id: str) -> list:
    """
    Retrieves all results from a completed batch.
    Results may come back in any order -- always use custom_id to match.
    """
    print(f"\n--- Retrieving Results for Batch {batch_id} ---")
    print("IMPORTANT: Results may be in ANY order. Use custom_id to match.\n")

    results = []
    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id
        result_type = result.result.type  # "succeeded" or "errored"

        if result_type == "succeeded":
            message = result.result.message
            text = next((b.text for b in message.content if hasattr(b, "text")), "(no text)")
            results.append({
                "custom_id": custom_id,
                "status": "succeeded",
                "text": text
            })
            print(f"  [{custom_id}] SUCCESS:")
            print(f"    {text.strip()[:120]}")
        else:
            error = result.result.error
            results.append({
                "custom_id": custom_id,
                "status": "errored",
                "error": str(error)
            })
            print(f"  [{custom_id}] ERROR: {error}")

    return results


# =====================================================================
# PART C: HANDLE FAILURES — RESUBMIT ONLY FAILED ITEMS
# =====================================================================
# When some requests in a batch fail, DO NOT resubmit the entire batch.
# Use custom_id to identify the failed requests and resubmit only those.
# Resubmitting the full batch wastes cost on requests that already succeeded.

def simulate_failure_recovery(results: list):
    """
    Shows the failure recovery pattern using custom_id.
    In this demo, we simulate 2 requests having failed.
    """
    print("\n--- PART C: Failure Recovery Pattern ---")

    # Simulate: pretend review-003 and review-005 failed
    simulated_failures = ["review-003", "review-005"]

    print(f"Suppose {simulated_failures} failed due to transient errors.")
    print("CORRECT recovery: resubmit ONLY the failed requests.\n")

    # Find the original requests for the failed custom_ids
    failed_requests = [
        req for req in BATCH_REQUESTS
        if req["custom_id"] in simulated_failures
    ]

    print(f"Would resubmit {len(failed_requests)} request(s):")
    for req in failed_requests:
        print(f"  {req['custom_id']}: {req['params']['messages'][0]['content'][:50]}...")

    print(f"""
EXAM PATTERNS:
  CORRECT: Parse output for failed custom_ids -> resubmit only those
  WRONG:   Resubmit the entire original batch (wastes cost on successes)
  WRONG:   Switch failed items to real-time API (loses 50% batch discount)
  WRONG:   Discard failed items (creates coverage gaps)

Modification on resubmit:
  If an item failed because the document exceeded the context limit,
  SPLIT the document into smaller chunks before resubmitting.
  Same custom_id strategy applies to the chunks.
""")


# =====================================================================
# PART D: BATCH VS. REAL-TIME DECISION FRAMEWORK
# =====================================================================

def explain_decision_framework():
    print("\n--- PART D: Batch vs. Real-Time Decision Framework ---")
    print("""
USE Batch API:                      DO NOT USE Batch API:
  Overnight technical debt report     Pre-merge code review (developers waiting)
  Weekly security audit               Real-time customer chat responses
  Nightly test generation             Interactive coding sessions
  Large-scale batch extraction        CI/CD pipeline steps that block deployment
  Non-blocking document analysis      Any workflow with an SLA under ~48 hours

The formula for when you CAN use batch:
  max_submission_interval = SLA_hours - 24h
  Example: 48h SLA -> submit every 24h
  Example: 30h SLA -> submit every 6h
  Example: 4h SLA  -> DO NOT USE BATCH (4 - 24 = negative, impossible)

Costs:
  Real-time API:  standard pricing (1x)
  Batch API:      50% of standard pricing (0.5x)
  Prompt cache reads: 10% of standard pricing (0.1x) <- cheapest

EXAM TRAP: "Batch API saves 90% like prompt caching"
WRONG: Batch saves 50%. Prompt cache READS save 90% (0.1x).
These are different mechanisms with different savings rates.

Limits:
  Max requests per batch: 100,000
  Max batch size: 256 MB
  custom_id: required for correlating results (results out of order)
  Multi-turn tool calling: NOT supported (each request is single-turn)
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 60)
    print("EXERCISE 4 -- Message Batches API (4.5)")
    print("=" * 60)
    print("""
This exercise submits a real 5-request batch, waits for results,
then demonstrates the failure recovery pattern.

PROMPT REFINEMENT BEFORE BATCH (exam concept):
  Before sending 10,000 requests to a batch, refine your prompt on a small
  sample (5-10 requests) and verify the output is what you expect.
  This exercise IS that sample run -- in production, you'd do this
  before submitting the full batch.
""")

    # Submit batch
    batch_id = submit_batch()

    # Wait for completion
    completed = wait_for_batch(batch_id)

    if completed:
        # Retrieve results
        results = retrieve_results(batch_id)
        # Show failure recovery pattern
        simulate_failure_recovery(results)
    else:
        print("\nBatch still processing. Showing failure recovery pattern with simulated data.")
        simulate_failure_recovery([])

    # Always show the decision framework
    explain_decision_framework()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 4.5")
    print("=" * 60)
    print("""
Batch API facts to memorize:
  Cost savings:  50% vs real-time (not 90% -- that's prompt caching)
  Processing:    Up to 24 hours, NO guaranteed latency SLA
  Ordering:      Results come back OUT of order -- always use custom_id
  Failures:      Resubmit ONLY failed items by custom_id
  Tool calling:  NOT supported for multi-turn within one request
  Limits:        100,000 requests OR 256MB per batch

Flags that DON'T exist:
  priority: critical   -- no priority flags in batch API
  /batch/{id}/expedite -- no expedite endpoint exists
""")


if __name__ == "__main__":
    main()
