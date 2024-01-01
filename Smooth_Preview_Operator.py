import bpy
def update_UI():

    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()

class SP_Set_Smooth(bpy.types.Operator):
    """Make Selected Object Smooth"""
    bl_idname = "vh.set_smooth"
    bl_label = "Set Smooth"

    smooth : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True
        if context.active_object is not None and context.active_object.mode == "SCULPT":
            return True

    def execute(self, context):

        preferences = context.preferences.addons[__package__].preferences

        for object in context.selected_objects:

            if object.type == "MESH":
                if any([m for m in object.modifiers if m.type == "SUBSURF"]):
                    for modifier in object.modifiers:
                        if modifier.type == "SUBSURF":

                            modifier.show_viewport =self.smooth
                            modifier.show_on_cage = self.smooth
                            modifier.show_render =self.smooth

                            modifier.levels =context.scene.subsurf_amt
                            modifier.render_levels = context.scene.subsurf_amt

                            if self.smooth:

                                curentmode = context.object.mode

                                if context.object.mode == "EDIT":
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                                if context.object.mode == "SCULPT":
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


                                if not preferences.No_Shade_Smooth:
                                    if not object.data.use_auto_smooth:
                                        bpy.ops.object.shade_smooth()

                                if curentmode == "EDIT":
                                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                if curentmode == "SCULPT":
                                    bpy.ops.object.mode_set(mode='SCULPT', toggle=False)
                            else:

                                curentmode = context.object.mode

                                if context.object.mode == "EDIT":
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                                if context.object.mode == "SCULPT":
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                                if not preferences.No_Shade_Smooth:
                                    if not object.data.use_auto_smooth:
                                        bpy.ops.object.shade_flat()

                                if curentmode == "EDIT":
                                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                if curentmode == "SCULPT":
                                    bpy.ops.object.mode_set(mode='SCULPT', toggle=False)

                else:
                    modifier = object.modifiers.new("Subdivision", "SUBSURF")

                    modifier.show_viewport =self.smooth
                    modifier.show_render =self.smooth
                    modifier.show_on_cage = self.smooth

                    modifier.levels =context.scene.subsurf_amt
                    modifier.render_levels = context.scene.subsurf_amt

                    curentmode = context.object.mode

                    if context.object.mode == "EDIT":
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                        if not preferences.No_Shade_Smooth:
                            if not object.data.use_auto_smooth:
                                bpy.ops.object.shade_smooth()



                    if context.object.mode == "SCULPT":
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                        if not preferences.No_Shade_Smooth:
                            if not object.data.use_auto_smooth:
                                bpy.ops.object.shade_smooth()

                    else:
                        if not preferences.No_Shade_Smooth:
                            if not object.data.use_auto_smooth:
                                bpy.ops.object.shade_smooth()

                    if curentmode == "EDIT":
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    if curentmode == "SCULPT":
                        bpy.ops.object.mode_set(mode='SCULPT', toggle=False)



                    update_UI()


        return {'FINISHED'}


class SP_Set_Smooth_Shortcut(bpy.types.Operator):
    """Make Selected Object Smooth"""
    bl_idname = "vh.set_smooth_s"
    bl_label = "Set Smooth"


    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True



    def execute(self, context):

        bpy.ops.vh.set_smooth(smooth=True)

        return {'FINISHED'}


class SP_Set_Normal_Shortcut(bpy.types.Operator):
    """Turn off Smooth"""
    bl_idname = "vh.set_normal_s"
    bl_label = "Set Normal"


    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True



    def execute(self, context):

        bpy.ops.vh.set_smooth(smooth=False)

        return {'FINISHED'}


class SP_Apply_Smooth(bpy.types.Operator):
    """Make Selected Object Smooth"""
    bl_idname = "vh.apply_smooth"
    bl_label = "Apply Smooth"


    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True


    def execute(self, context):

        save_active = bpy.context.view_layer.objects.active

        for object in context.selected_objects:

            bpy.context.view_layer.objects.active = object

            if object.type == "MESH":

                if any([m for m in object.modifiers if m.type == "SUBSURF"]):
                    for modifier in object.modifiers:
                        if modifier.type == "SUBSURF":

                            bpy.ops.object.modifier_apply(modifier=modifier.name)

                            update_UI()
        try:
            bpy.context.view_layer.objects.active = save_active
        except:
            pass

        return {'FINISHED'}



class SP_Set_Smooth_Menu(bpy.types.Menu):
    bl_label = "SetSmooth_Menu"
    bl_idname = "SP_MT_SetSmooth_Menu"

    def draw(self, context):
        layout = self.layout

        preferences = context.preferences.addons[__package__].preferences
        layout.prop(context.scene, "subsurf_amt", text="Levels")
        layout.prop(preferences, "No_Shade_Smooth", text="Disable Shade Smooth / Flat")

        layout.operator("vh.apply_smooth", text="Apply")


class SP_Toogle_Modifier_Menu(bpy.types.Menu):
    bl_label = "Toogle Modifier Menu"
    bl_idname = "SP_MT_Toogle_Modifier_Menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "target_modifier", text="Filter")


        apply = layout.operator("vh.apply_modifier", text="Apply")
        apply.limit = context.scene.target_modifier
        apply.remove= False

        apply = layout.operator("vh.apply_modifier", text="Remove")
        apply.limit = context.scene.target_modifier
        apply.remove= True

class SP_Edit_Modifier(bpy.types.Operator):
    """Apply Selected Modifier"""
    bl_idname = "vh.apply_modifier"
    bl_label = "Apply Modifier"

    limit : bpy.props.StringProperty()
    remove: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True
        if context.active_object is not None and context.active_object.mode == "SCULPT":
            return True

    def execute(self, context):


        save_active = bpy.context.view_layer.objects.active

        for object in context.selected_objects:

            bpy.context.view_layer.objects.active = object

            if object.type == "MESH" and object.modifiers:

                for modifier in object.modifiers:



                    if self.limit == "ALL":
                        if self.remove:
                            bpy.ops.object.modifier_remove(modifier=modifier.name)
                        else:
                            bpy.ops.object.modifier_apply(modifier=modifier.name)
                        update_UI()

                    if modifier.type == self.limit:
                        if self.remove:
                            bpy.ops.object.modifier_remove(modifier=modifier.name)
                        else:
                            bpy.ops.object.modifier_apply(modifier=modifier.name)
                        update_UI()

        try:
            bpy.context.view_layer.objects.active = save_active
        except:
            pass

        return {'FINISHED'}



class SP_Modifier_Toogle(bpy.types.Operator):
    """Toogle Modifier"""
    bl_idname = "vh.toogle_modifier"
    bl_label = "Toogle Modifier"

    state : bpy.props.BoolProperty()
    limit : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):

        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True
        if context.active_object is not None and context.active_object.mode == "SCULPT":
            return True

    def execute(self, context):


        for object in context.selected_objects:

            if object.type == "MESH":
                if object.modifiers:

                    for modifier in object.modifiers:

                        if self.limit == "ALL":
                            modifier.show_viewport = self.state
                            modifier.show_render =self.state
                            update_UI()

                        elif modifier.type == self.limit:

                                modifier.show_viewport = self.state
                                modifier.show_render =self.state
                                update_UI()


        return {'FINISHED'}






def draw_item(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.prop(context.space_data.overlay, "show_wireframes", text="", icon="FILE_3D")


    preferences = context.preferences.addons[__package__].preferences


    if preferences.Set_Smooth_Button:
        row.operator("vh.set_smooth", text="Smooth").smooth=True
        row.operator("vh.set_smooth", text="Normal").smooth=False
        row.menu("SP_MT_SetSmooth_Menu", text="", icon="DOWNARROW_HLT")
        row.separator()

    if preferences.Modifier_Button:

        modifier_toogle_off = row.operator("vh.toogle_modifier", text="Modifier On")
        modifier_toogle_off.state=True
        modifier_toogle_off.limit=context.scene.target_modifier

        modifier_toogle_on = row.operator("vh.toogle_modifier", text="Modifier Off")
        modifier_toogle_on.state=False
        modifier_toogle_on.limit =context.scene.target_modifier

        row.menu("SP_MT_Toogle_Modifier_Menu", text="", icon="DOWNARROW_HLT")


modifier_list = [modifier.identifier for modifier in bpy.types.Modifier.bl_rna.properties['type'].enum_items]
modifier_list.insert(0, "ALL")
modifier_enum = []

for modifier in modifier_list:
    modifier_enum.append((modifier, modifier.title().replace("_", " "), modifier))



classes = [SP_Set_Smooth, SP_Modifier_Toogle, SP_Set_Smooth_Menu, SP_Apply_Smooth, SP_Set_Normal_Shortcut, SP_Set_Smooth_Shortcut, SP_Toogle_Modifier_Menu, SP_Edit_Modifier]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.subsurf_amt = bpy.props.IntProperty(name="", default=1, min=0, soft_max = 4)
    # bpy.types.Scene.Modifier_Button = bpy.props.BoolProperty(default=True)
    # bpy.types.Scene.Set_Smooth_Button = bpy.props.BoolProperty(default=True)

    bpy.types.Scene.target_modifier = bpy.props.EnumProperty(items=modifier_enum)

    bpy.types.VIEW3D_HT_header.append(draw_item)

def unregister():


    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(draw_item)

    del bpy.types.Scene.subsurf_amt
    # del bpy.types.Scene.Modifier_Button
    # del bpy.types.Scene.Set_Smooth_Button


if __name__ == "__main__":
    register()
