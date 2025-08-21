import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

WEEKEND = {5, 6}  # Saturday=5, Sunday=6 (Python weekday: Monday=0)

def count_workdays(start, end):
    n = 0
    cur = start
    while cur <= end:
        if cur.weekday() not in WEEKEND:
            n += 1
        cur += timedelta(days=1)
    return n

class LeaveRequest(Document):
    def validate(self):
        if not self.from_date or not self.to_date:
            return

        from_date = datetime.strptime(str(self.from_date), "%Y-%m-%d").date()
        to_date = datetime.strptime(str(self.to_date), "%Y-%m-%d").date()

        if from_date > to_date:
            frappe.throw("From Date must be before To Date.")

        days_inclusive = (to_date - from_date).days + 1
        if days_inclusive > 5:
            frappe.throw("Total number of leave days must not exceed 5 days.")

        self.total_days = count_workdays(from_date, to_date)


@frappe.whitelist()
def approve_leave(docname: str):
    """Approve a pending leave request. Only HR Manager can approve.
    Sets status to Approved and approved_by to current user.
    """
    if not frappe.has_role("HR Manager"):
        frappe.throw("Not permitted: only HR Manager can approve.")

    doc = frappe.get_doc("Leave Request", docname)
    if doc.status != "Pending":
        frappe.throw("Only Pending requests can be approved.")

    doc.status = "Approved"
    doc.approved_by = frappe.session.user
    doc.save()
    frappe.db.commit()
    return {"status": doc.status, "approved_by": doc.approved_by}