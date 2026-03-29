import sqlite3


def top_departments(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.name, SUM(e.salary) AS total_salary
            FROM departments d
            JOIN employees e
              ON d.dept_id = e.dept_id
            GROUP BY d.dept_id, d.name
            ORDER BY total_salary DESC, d.name ASC
            LIMIT 3
        """)
        return cur.fetchall()


def employees_with_projects(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT e.name, p.name
            FROM employees e
            JOIN project_assignments pa
              ON e.emp_id = pa.emp_id
            JOIN projects p
              ON pa.project_id = p.project_id
            ORDER BY e.name ASC, p.name ASC
        """)
        return cur.fetchall()


def salary_rank_by_department(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT employee_name, dept_name, salary, salary_rank
            FROM (
                SELECT
                    e.name AS employee_name,
                    d.name AS dept_name,
                    e.salary AS salary,
                    RANK() OVER (
                        PARTITION BY e.dept_id
                        ORDER BY e.salary DESC
                    ) AS salary_rank
                FROM employees e
                JOIN departments d
                  ON e.dept_id = d.dept_id
            )
            ORDER BY dept_name ASC, salary_rank ASC, employee_name ASC
        """)
        return cur.fetchall()