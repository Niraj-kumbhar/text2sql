## `salaries`

- **Description**: Details the salary history of each employee.
- **Composite Primary Key**: `emp_no`, `from_date`
- **Foreign Key**:
    - `emp_no`: References `employees(emp_no)`

### Columns:
- `emp_no`: Employee number.
- `salary`: Salary amount.
- `from_date`: Start date of the salary period.
- `to_date`: End date of the salary period.