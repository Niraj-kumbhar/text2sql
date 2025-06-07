## `titles`

- **Description**: Tracks the job titles held by employees over time.
- **Composite Primary Key**: `emp_no`, `from_date`
- **Foreign Key**:
    - `emp_no`: References `employees(emp_no)`

### Columns:
- `emp_no`: Employee number.
- `title`: Job title.
- `from_date`: Start date of the title.
- `to_date`: End date of the title.