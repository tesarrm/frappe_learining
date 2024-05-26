from os import stat
import frappe

@frappe.whitelist(allow_guest=True)
def get_all_items(group):
    items = frappe.db.sql(
        f"""
        SELECT name, item_name, description 
        FROM `tabItem` 
        WHERE item_group = '{group}' ;
        """, 
        as_dict=True
    )

    if(items):
        status_code = 200
        body = items
    else: 
        status_code = 400
        body = "The item you are looking for this list not found!"

    response = dict(
        status_code = status_code,
        body = body
    )

    return response

@frappe.whitelist()
def add_item(code, name, group, uom):
    add_item = frappe.get_doc({
        "doctype": "Item", 
        "item_code": code,
        "item_name": name,
        "item_group": group,
        "stock_uom": uom
    })

    add_item.insert()
    frappe.db.commit()

    add_new_note(name, group)

    return add_item

@frappe.whitelist()
def update_item(name, new_item_name):
    frappe.db.sql(
        f"""
        UPDATE `tabItem`
        SET item_name = '{new_item_name}' 
        WHERE name = '{name}';
        """  
    )

    frappe.db.commit()

    return "Success"

@frappe.whitelist()
def delete_item(name):
    frappe.db.sql(
        f"""
        DELETE FROM `tabItem`
        WHERE name = '{name}'
        """
    )

    frappe.db.commit()

    return "Success"

##

def add_new_note(name, group):
    title = f"{name} has been added to items"
    content = f"A new item with the name {name} has been added to {group}"

    add_note = frappe.get_doc({
        "doctype": "Note",
        "title": title, 
        "content": content 
    })

    add_note.insert()
    frappe.db.commit()