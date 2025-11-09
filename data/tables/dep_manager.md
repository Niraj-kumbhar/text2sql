## Table Name: `dept_manager`

- **Description**: Records the managerial assignments of employees to departments.
- **Composite Primary Key**: `dept_no`, `emp_no`, `from_date`
- **Foreign Keys**:
    - `dept_no`: References `departments(dept_no)`
    - `emp_no`: References `employees(emp_no)`

### Columns:
- `dept_no`: Department number.
- `emp_no`: Employee number.
- `from_date`: Start date of the managerial assignment.
- `to_date`: End date of the managerial assignment.