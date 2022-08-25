# Extract scores from scores Excel file
Quera.ir and lms.sbu.ac.ir would let us download scores as a complicated Excel file, but we want to enter scores to another sheet with different structure.

This script also need a sorted list of student IDs, so it can print scores in desired order. (Placed in `students.txt`)

Example:
```bash
python3 ./quera.py --file hw1_quera.xlsx
python3 ./lms.py --file hw1_lms.xlsx

```

