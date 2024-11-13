button_dict = {}

def on_value_changed():
    pass

for i in range(1, 3):
        button_dict[f'Camera {i}'] = on_value_changed()

print(button_dict)