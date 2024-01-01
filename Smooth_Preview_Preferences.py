import bpy
from . Smooth_Preview_Operator import *
import rna_keymap_ui




class SP_user_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    Modifier_Button : bpy.props.BoolProperty(default=True)
    Set_Smooth_Button : bpy.props.BoolProperty(default=True)
    No_Shade_Smooth: bpy.props.BoolProperty(default=False)


    def draw(self, context):



        layout = self.layout

        wm = bpy.context.window_manager
        box = layout.box()
        split = box.split()
        col = split.column()
        col.separator()


        # keymap = context.window_manager.keyconfigs.user.keymaps['3D View']
        # keymap_items = keymap.keymap_items
        # km = keymap.active()



        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        km = kc.keymaps['3D View']
        kmi = km.keymap_items["vh.set_smooth_s"]
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry")

        km = kc.keymaps['3D View']
        kmi = km.keymap_items["vh.set_normal_s"]
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry")


        col.prop(self, "Modifier_Button", text="Use Modifier Buttons")
        col.prop(self, "Set_Smooth_Button", text="Use Smooth Preview Buttons")
        col.prop(self, "No_Shade_Smooth", text="Disable Shade Smooth / Flat")

addon_keymaps = []



def get_addon_preferences():
    ''' quick wrapper for referencing addon preferences '''
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences


def get_hotkey_entry_item(km, kmi_name, kmi_value):
    '''
    returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
    if there are multiple hotkeys!)
    '''
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].properties.name == kmi_value:
                return km_item
    return None



def add_hotkey():
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons["Smooth_Preview"].preferences

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')

    kmi = km.keymap_items.new("vh.set_normal_s", type="F1", value="PRESS")

    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("vh.set_smooth_s", type="F1", value="PRESS", ctrl=True)

    addon_keymaps.append((km, kmi))

class Template_Add_Hotkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "template.add_hotkey"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()
        # self.report({'INFO'}, "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}

def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

        # wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()



classes = [SP_user_preferences, Template_Add_Hotkey]

def register():

    add_hotkey()



    for cls in classes:
        bpy.utils.register_class(cls)




    pass


def unregister():

    remove_hotkey()

    for cls in classes:
        bpy.utils.unregister_class(cls)



    pass

if __name__ == "__main__":
    register()
