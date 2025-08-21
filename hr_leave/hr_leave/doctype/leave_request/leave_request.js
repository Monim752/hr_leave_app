frappe.ui.form.on('Leave Request', {
    refresh(frm) {
        // Show Approve button only for HR Manager and when status is Pending
        if (frm.doc.status === 'Pending' && frappe.user_roles.includes('HR Manager')) {
            frm.add_custom_button(__('Approve'), () => {
                frappe.call({
                    method: 'hr_leave.hr_leave.doctype.leave_request.leave_request.approve_leave',
                    args: { docname: frm.doc.name },
                    freeze: true,
                }).then(r => {
                    frm.reload_doc();
                    frappe.show_alert({message: __('Leave Approved'), indicator: 'green'});
                });
            }).addClass('btn-primary');
        }
    },

    leave_type(frm) {
        if (frm.doc.leave_type === 'EL') {
            frappe.msgprint(__('Earned Leave requires manager approval.'));
        }
    },

    from_date(frm) { recalc_total_days(frm); },
    to_date(frm) { recalc_total_days(frm); },
});

function recalc_total_days(frm) {
    const from_date = frm.doc.from_date;
    const to_date = frm.doc.to_date;
    if (!from_date || !to_date) return;

    const start = frappe.datetime.str_to_obj(from_date);
    const end = frappe.datetime.str_to_obj(to_date);
    if (start > end) {
        frm.set_value('total_days', null);
        return;
    }

    let count = 0;
    const cur = new Date(start);
    while (cur <= end) {
        const wd = cur.getDay(); // 0=Sun,...,6=Sat
        if (wd !== 0 && wd !== 6) count += 1; // exclude weekend (Sat=6, Sun=0)
        cur.setDate(cur.getDate() + 1);
    }
    frm.set_value('total_days', count);
}