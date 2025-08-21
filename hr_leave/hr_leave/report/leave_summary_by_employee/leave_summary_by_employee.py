import frappe

def execute(filters=None):
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 200},
        {"label": "Total Leave Requests", "fieldname": "total", "fieldtype": "Int", "width": 180},
        {"label": "Approved Leaves", "fieldname": "approved", "fieldtype": "Int", "width": 160},
        {"label": "Rejected Leaves", "fieldname": "rejected", "fieldtype": "Int", "width": 160},
    ]

    data = frappe.db.sql(
        """
        SELECT
            lr.employee as employee,
            COUNT(*) as total,
            SUM(CASE WHEN lr.status = 'Approved' THEN 1 ELSE 0 END) as approved,
            SUM(CASE WHEN lr.status = 'Rejected' THEN 1 ELSE 0 END) as rejected
        FROM `tabLeave Request` lr
        GROUP BY lr.employee
        ORDER BY lr.employee
        """,
        as_dict=True,
    )

    return columns, data