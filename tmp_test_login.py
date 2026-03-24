from main import BlazeBiteApp, STORE_LABELS

app = BlazeBiteApp()
store_label = 'Fast Food'
store_key = next((k for k, v in STORE_LABELS.items() if v == store_label), None)
role = 'attendant'
username = 'ff_attendant'
password = 'ff_pass'

user_row = app.db.get_user(store_key, role)
print('user_row', user_row)

if not user_row or user_row[1] != username or user_row[2] != password:
    print('login failed')
else:
    app.active_store = store_key
    app.current_role = role
    app.admin_logged_in = (role == 'admin')
    app.menu_data = app._load_menu()
    app.order_counter = app._get_next_order_number()
    app.active_category = next(iter(app.menu_data.keys()), None)
    print('login success', app.active_store, app.current_role, app.active_category)
    print('categories', list(app.menu_data.keys()))
    app._show_view('pos')
    print('view set to', app.active_tab)

app.destroy()
