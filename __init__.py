bl_info = {
    "name": "Smooth Preview",
    "author": "BlenderBoi",
    "version": (1, 4),
    "blender": (4, 0, 0),
    "description": "Smooth Preview that acts similar like in maya 3",
    "wiki_url": "",
    "category": "Utility",
}


import bpy
from . import Smooth_Preview_Operator
from . import Smooth_Preview_Preferences


def register():

    Smooth_Preview_Operator.register()
    Smooth_Preview_Preferences.register()


def unregister():

    Smooth_Preview_Operator.unregister()
    Smooth_Preview_Preferences.unregister()



if __name__ == "__main__":
    register()
