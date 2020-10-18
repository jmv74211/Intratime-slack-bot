def get_clock_ui():
    return {
        "title": "Intratime: Clocking",
        "submit_label": "Submit",
        "callback_id": "clock",
        "elements": [
            {
                "label": "Action",
                "type": "select",
                "name": "action",
                "options": [
                    {
                        "label": "IN",
                        "value": "in"
                    },
                    {
                        "label": "PAUSE",
                        "value": "pause"
                    },
                    {
                        "label": "RETURN",
                        "value": "return"
                    },
                    {
                        "label": "OUT",
                        "value": "out"
                    }
                ]
            }
        ]
    }

# ----------------------------------------------------------------------------------------------------------------------


def get_sign_up_ui():
    return {
        "title": "Intratime: Sign up",
        "submit_label": "Submit",
        "callback_id": "sign_up",
        "elements": [
            {
                "label": "Intratime email",
                "name": "email",
                "type": "text",
                "subtype": "email",
                "placeholder": "you@example.com"
            },
            {
                "label": "Intratime password",
                "name": "password",
                "type": "text",
                "placeholder": "password",
                "hint": "Attention: There is no password field type, so it will be written in plain text"
            }
        ]
    }

# ----------------------------------------------------------------------------------------------------------------------


def get_update_user_ui():
    return {
        "title": "Intratime: Update user",
        "submit_label": "Submit",
        "callback_id": "update_user",
        "elements": [
            {
                "label": "Email Address",
                "name": "email",
                "type": "text",
                "subtype": "email",
                "placeholder": "you@example.com"
            },
            {
                "label": "Password",
                "name": "password",
                "type": "text",
                "placeholder": "password",
                "hint": "Attention: There is no password field type, so it will be written in plain text"

            }
        ]
    }

# ----------------------------------------------------------------------------------------------------------------------


def get_delete_user_ui():
    return {
        "title": "Intratime: Delete user",
        "submit_label": "Submit",
        "callback_id": "delete_user",
        "elements": [
            {
                "label": "Are you sure you want to delete your user?",
                "type": "select",
                "name": "delete",
                "options": [
                    {
                        "label": "No",
                        "value": "no"
                    },
                    {
                        "label": "Yes",
                        "value": "yes"
                    }
                ]
            }
        ]
    }
