## Table Name: `dept_emp`

- **Description**: Associates employees with the departments they have worked in, including the duration.
- **Composite Primary Key**: `emp_no`, `dept_no`, `from_date`
- **Foreign Keys**:
    - `emp_no`: References `employees(emp_no)`
    - `dept_no`: References `departments(dept_no)`

### Columns:
- `emp_no`: Employee number.
- `dept_no`: Department number.
- `from_date`: Start date of the department assignment.
- `to_date`: End date of the department assignment.