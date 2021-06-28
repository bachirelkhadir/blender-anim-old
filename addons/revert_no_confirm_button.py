#!/usr/bin/env python3

import bpy

bl_info = {
    "name": "Revert no confirm",
    "category": "Object",
}



class RevertNoConfirmOp(bpy.types.Operator):

    bl_idname = "wm.revert_no_confirm"
    bl_label = "Revert No Confirm"
    def execute(self, context):
        print("Reverting without confirmation")
        bpy.ops.wm.revert_mainfile()
        return {'FINISHED'}



class RevertNoConfirmPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Rev (no confirm)"
    bl_idname = "OBJECT_PT_revertnoconfirm"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.revert_no_confirm")



def register():
    print("registering revert no confirm op")
    bpy.utils.register_class(RevertNoConfirmOp)
    bpy.utils.register_class(RevertNoConfirmPanel)


def unregister():

    print("unregistering revert no confirm op")
    bpy.utils.unregister_class(RevertNoConfirmOp)
    bpy.utils.unregister_class(RevertNoConfirmPanel)


if __name__ == "__main__":
    register()
