#!/bin/bash
file="C:\Users\zac.ramsey\Desktop\Ramsey-Brain/raw/cca_f_question_bank_v1.0.0.md"

# Get all line numbers where Domain 1 questions appear
sed -n '/^## q-.*\n_subdomain: 1\.[1-7]/p' "$file" | while IFS= read -r line; do
  echo "$line"
done
