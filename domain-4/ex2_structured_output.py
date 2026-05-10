"""
CCA-F Domain 4, Exercise 2 — Structured Output and JSON Schemas (Subdomain 4.3)
================================================================================

WHAT THIS EXERCISES:
  tool_use with a JSON schema is the most reliable way to get structured output.
  Schema compliance guarantees SYNTAX correctness only -- not SEMANTIC correctness.
  Semantic errors require programmatic validation on top of schema conformance.

KEY RULES:
  - tool_use + JSON schema = eliminates JSON syntax errors
  - Nullable fields for optional data -- prevents model from fabricating values
  - enum + "other" + detail field for extensible categories
  - "unclear" enum value for genuinely ambiguous cases
  - conflict_detected boolean to flag self-correction opportunities
  - Schema CANNOT catch: totals that don't add up, wrong field values, fabricated data
  - Semantic errors need application-layer checks (cross-field validation, range checks)

STRUCTURE:
  Part A -- Schema design: nullable fields, enum patterns, self-correction fields
  Part B -- Extraction in action: what schema-valid but semantically wrong looks like
  Part C -- Semantic validation layer: catching what schema cannot
"""

import sys
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
# PART A: SCHEMA DESIGN
# =====================================================================
# This schema demonstrates all the key design patterns:
#   1. Nullable fields for optional data (purchase_order, discount_code)
#      -- if field is required and data is absent, model fabricates a value
#   2. enum + "other" + detail field (payment_method, currency)
#      -- captures known values cleanly; handles unknowns with "other" + detail
#   3. "unclear" as an enum option (document_type)
#      -- gives model an honest escape hatch instead of forcing a wrong guess
#   4. Both stated_total AND calculated_total
#      -- enables self-correction: if they differ, flag the discrepancy
#   5. conflict_detected boolean
#      -- explicit machine-readable flag for downstream routing to human review

INVOICE_EXTRACTION_TOOL = {
    "name": "extract_invoice",
    "description": (
        "Extract structured data from an invoice document. "
        "Use null for any field where the information is not present in the document. "
        "Do not fabricate or infer values that are not explicitly stated."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor_name": {
                "type": "string",
                "description": "Name of the company or person that issued the invoice"
            },
            "invoice_number": {
                # Nullable -- some invoices don't have invoice numbers
                "type": ["string", "null"],
                "description": "Invoice identifier if present, null if not stated"
            },
            "invoice_date": {
                "type": ["string", "null"],
                "description": "Invoice date in YYYY-MM-DD format if present, null otherwise"
            },
            "stated_total": {
                "type": "number",
                "description": "The total amount as written on the invoice"
            },
            "calculated_total": {
                "type": "number",
                "description": "Sum of all line item amounts (calculated independently)"
            },
            "currency": {
                # enum + "other" pattern -- covers common values, handles unknowns
                "type": "string",
                "enum": ["USD", "EUR", "GBP", "JPY", "CAD", "other"],
                "description": "Currency code. Use 'other' if currency is not in the list."
            },
            "currency_detail": {
                # Only needed when currency is "other"
                "type": ["string", "null"],
                "description": "Specify currency here if currency field is 'other', else null"
            },
            "payment_method": {
                "type": ["string", "null"],
                "enum": ["credit_card", "bank_transfer", "check", "paypal", "other", None],
                "description": "Payment method if stated, null if not mentioned"
            },
            "document_type": {
                # "unclear" gives model an honest option for ambiguous cases
                "type": "string",
                "enum": ["invoice", "receipt", "credit_note", "proforma", "unclear"],
                "description": "Type of document. Use 'unclear' if the document type is ambiguous."
            },
            "confidence": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Your confidence in the extraction accuracy"
            },
            "conflict_detected": {
                "type": "boolean",
                "description": "True if stated_total does not match calculated_total, or if source data is inconsistent"
            }
        },
        "required": [
            "vendor_name", "stated_total", "calculated_total",
            "currency", "document_type", "confidence", "conflict_detected"
        ]
    }
}


# =====================================================================
# SAMPLE DOCUMENTS
# =====================================================================

GOOD_INVOICE = """
INVOICE #INV-2026-0042
Acme Corp
Date: March 15, 2026

Items:
  Widget A (x2) ....... $89.98
  Widget B (x1) ....... $45.00
  Shipping ............. $12.50

TOTAL: $147.48
Payment: Bank Transfer
"""

AMBIGUOUS_INVOICE = """
Acme Corp
March 2026

Widget A x2: $89.98
Widget B: $45.00
Shipping: $12.50

Amount Due: $200.00
"""
# Note: stated_total ($200.00) does not match calculated total ($147.48)
# This should trigger conflict_detected = true

MINIMAL_RECEIPT = """
Thank you for your purchase!
Acme Store
Total: 50 EUR
"""
# Many optional fields are absent -- nullable fields prevent fabrication


# =====================================================================
# PART B: EXTRACTION IN ACTION
# =====================================================================

def extract_invoice(document: str, label: str) -> dict:
    """Extracts invoice data using tool_use with the JSON schema."""
    print(f"\n  Extracting: {label}")

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=[INVOICE_EXTRACTION_TOOL],
        # Force the model to call this specific tool -- no text response allowed
        tool_choice={"type": "tool", "name": "extract_invoice"},
        messages=[{"role": "user", "content": f"Extract data from this document:\n\n{document}"}]
    )

    # Find the tool_use block in the response
    for block in response.content:
        if block.type == "tool_use":
            data = block.input
            print(f"  vendor_name:      {data.get('vendor_name')}")
            print(f"  invoice_number:   {data.get('invoice_number')} (null = not found, not fabricated)")
            print(f"  stated_total:     {data.get('stated_total')}")
            print(f"  calculated_total: {data.get('calculated_total')}")
            print(f"  currency:         {data.get('currency')}")
            print(f"  document_type:    {data.get('document_type')}")
            print(f"  confidence:       {data.get('confidence')}")
            print(f"  conflict_detected:{data.get('conflict_detected')} <- True if totals don't match")
            return data

    print("  ERROR: No tool_use block in response")
    return {}


# =====================================================================
# PART C: SEMANTIC VALIDATION
# =====================================================================
# Schema compliance (guaranteed by tool_use) eliminates syntax errors.
# But the model can still produce schema-valid JSON with semantic errors.
# Example: totals that don't add up, dates in wrong ranges, etc.
# Application-layer validation catches what schema cannot.

def validate_extraction(data: dict) -> list:
    """
    Semantic validation layer -- catches errors schema cannot prevent.
    Returns a list of validation error messages.
    """
    errors = []

    # Cross-field check: do the totals agree?
    stated = data.get("stated_total")
    calculated = data.get("calculated_total")
    if stated is not None and calculated is not None:
        if abs(stated - calculated) > 0.02:  # $0.02 tolerance for rounding
            errors.append(
                f"Total mismatch: stated=${stated:.2f} vs calculated=${calculated:.2f} "
                f"(difference: ${abs(stated - calculated):.2f})"
            )

    # Consistency check: conflict_detected flag should match actual discrepancy
    has_discrepancy = (stated is not None and calculated is not None and
                       abs(stated - calculated) > 0.02)
    if has_discrepancy and not data.get("conflict_detected"):
        errors.append("conflict_detected should be True (totals disagree) but is False")

    # Range check: totals should be positive
    if stated is not None and stated < 0:
        errors.append(f"stated_total is negative: {stated}")

    # Currency detail required when currency is "other"
    if data.get("currency") == "other" and not data.get("currency_detail"):
        errors.append("currency is 'other' but currency_detail is null -- detail required")

    return errors


def main():
    print("=" * 60)
    print("EXERCISE 2 -- Structured Output and JSON Schemas (4.3)")
    print("=" * 60)

    print("\n--- PART A: Schema Design (see INVOICE_EXTRACTION_TOOL above) ---")
    print("""
Key design decisions in this schema:
  - invoice_number: nullable string (not required string)
    Reason: some invoices have no number; required field = model fabricates one
  - currency: enum with "other" + currency_detail field
    Reason: handles known values cleanly; captures unknowns without fabrication
  - stated_total AND calculated_total (both required)
    Reason: cross-validation catches discrepancies
  - conflict_detected: boolean
    Reason: machine-readable flag for routing to human review
  - confidence: high/medium/low enum
    Reason: model's self-assessment; calibrate thresholds with labeled validation sets
""")

    print("\n--- PART B: Extraction in Action ---")
    data_good = extract_invoice(GOOD_INVOICE, "Well-formed invoice")
    data_ambiguous = extract_invoice(AMBIGUOUS_INVOICE, "Invoice with total mismatch")
    data_minimal = extract_invoice(MINIMAL_RECEIPT, "Minimal receipt (many fields absent)")

    print("\n--- PART C: Semantic Validation ---")
    for label, data in [
        ("Good invoice", data_good),
        ("Ambiguous invoice", data_ambiguous),
        ("Minimal receipt", data_minimal),
    ]:
        if data:
            errors = validate_extraction(data)
            status = "PASS" if not errors else "FAIL"
            print(f"\n  [{status}] {label}")
            for err in errors:
                print(f"    ERROR: {err}")
            if not errors:
                print(f"    All semantic checks passed")

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 4.3")
    print("=" * 60)
    print("""
tool_use + JSON schema guarantees:
  - Schema-compliant output on stop_reason "end_turn"
  - No JSON syntax errors
  - Required fields are present
  - Enum values are from the allowed list

tool_use + JSON schema does NOT guarantee:
  - Semantic correctness (values that make business sense)
  - Accurate data (model can still fabricate schema-valid values)
  - Cross-field consistency (totals matching, dates in range)

Schema design rules:
  - Nullable fields for any data that might be absent (prevents fabrication)
  - Required fields only for data guaranteed to exist in every document
  - enum + "other" + detail for extensible categories
  - "unclear" enum value for genuinely ambiguous cases (honest escape hatch)
  - Both stated_total AND calculated_total for self-correction capability

Semantic validation (application layer):
  - Cross-field checks: do line items sum to total?
  - Range checks: is the amount non-negative?
  - Date logic: is due_date after invoice_date?
  - Reference validation: does order_id match expected format?

WRONG: "strict:true eliminates all errors" -- only syntax errors, not semantic
WRONG: "required fields with 'N/A' string" -- use nullable instead
WRONG: stop_reason "max_tokens" guarantees schema compliance -- it does NOT
""")


if __name__ == "__main__":
    main()
