from rox import g, OptionsBox
from location_search_dialog import LocationSearchDialog


def register():
    def build_location_option_widget(box, node, label, option):
        label_widget = g.Label(label)
        value_widget = g.Label()
        button = g.Button(stock=g.STOCK_FIND)
        box.may_add_tip(button, node)
    
        box.handlers[option] = (lambda: str(value_widget.get_label()), 
                                lambda: value_widget.set_label(option.value))
    
        def button_clicked(button):
            def dialog_response(dialog, response):
                if response == g.RESPONSE_ACCEPT:
                    selection = dialog.result_list.get_selection()
                    model, it = selection.get_selected()
                    if it:
                        code = model.get_value(it, 1)
                        if code:
                            name = str(model.get_value(it, 0))
                            value_widget.set_label("%s (%s)" % (str(code), name))
                dialog.destroy()
                box.check_widget(option)
            dialog = LocationSearchDialog()
            dialog.connect('response', dialog_response)
            dialog.show()
    
        button.connect('clicked', button_clicked)
    
        hbox = g.HBox(spacing = 5)
        hbox.pack_start(label_widget)
        hbox.pack_start(value_widget)
        hbox.pack_start(button)
    
        return [hbox]
    
    OptionsBox.widget_registry['location_search'] = build_location_option_widget
