bl_info = {
    "name": "Cynthia",
    "author": "Ian Ichung'wa Karanja (ranjian0)",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Toolshelf > Cynthia",
    "description": "Building Generation Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

import bpy
from bpy.props import *

from .core import register_core, unregister_core
from .cynthia_window import Window
from .cynthia_door import Door
from .cynthia_balcony import *
from .cynthia_rails import *
from .cynthia_roof import *
from .cynthia_staircase import *
from .cynthia_stairs import *
from .cynthia_update import update_building
from .utils import (
        facedata_from_index,
        Template_Modal_OP)

# =======================================================
#
#           PROPERTY GROUPS
#
# =======================================================

class SplitProperty(bpy.types.PropertyGroup):
    amount  = FloatVectorProperty(
        name="Split Amount", description="How much to split geometry", min=.01, max=2.99,
        subtype='XYZ', size=2, default=(2.0, 2.7),
        update=update_building)

    off     = FloatVectorProperty(
        name="Split Offset", description="How much to offset geometry", min=-1000.0, max=1000.0,
        subtype='TRANSLATION', size=3, default=(0.0, 0.0, 0.0),
        update=update_building)

    collapsed = BoolProperty()

    def draw(self, context, layout, parent):
        box = layout.box()
        if parent.has_split:
            row = box.row(align=True)
            row.prop(parent, 'has_split', toggle=True)
            _icon = 'INLINK' if not self.collapsed else 'LINK'
            row.prop(self, 'collapsed', text="", icon=_icon)

            if not self.collapsed:
                col = box.column(align=True)
                col.prop(self, 'amount', slider=True)

                col = box.column(align=True)
                col.prop(self, 'off')
        else:
            box.prop(parent, 'has_split', toggle=True)

class BalconyProperty(bpy.types.PropertyGroup):
    # Balcony Options
    width = FloatProperty(
        name="Balcony Width", description="Width of balcony", min=0.01, max=100.0, default=2)

    railing = BoolProperty(
        name="Add Railing", description="Whether the balcony has railing", default=True)

    # Balcony Split Options
    has_split = BoolProperty(
        name="Add Split", description="Whether to split the balcony face", default=False)
    split = PointerProperty(type=SplitProperty)

    # Rail Options
    pw = FloatProperty(name="Post Width", description="Width of each post",
                       min=0.01, max=100.0, default=0.15)

    ph = FloatProperty(
        name="Post Height", description="Height of each post", min=0.01, max=100.0, default=0.7)

    pd = FloatProperty(name="Post Desnsity", description="Number of posts along each edge", min=0.0, max=1.0,
                       default=0.9)

    rw = FloatProperty(name="Rail Width", description="Width of each rail",
                       min=0.01, max=100.0, default=0.15)

    rh = FloatProperty(name="Rail Height", description="Height of each rail",
                       min=0.01, max=100.0, default=0.025)

    rd = FloatProperty(name="Rail Desnsity", description="Number of rails over each edge", min=0.0, max=1.0,
                       default=0.2)

    ww = FloatProperty(name="Wall Width", description="Width of each wall",
                       min=0.01, max=100.0, default=0.075)

    wh = FloatProperty(
        name="Wall Height", description="Height of each wall", min=0.01, max=100.0, default=0.7)

    cpw = FloatProperty(name="Corner Post Width", description="Width of each corner post", min=0.01, max=100.0,
                        default=0.15)

    cph = FloatProperty(name="Corner Post Height", description="Height of each corner post", min=0.01, max=100.0,
                        default=0.7)

    hcp = BoolProperty(
        name="Corner Posts", description="Whether the railing has corner posts", default=True)

    df = BoolProperty(name="Delete Faces",
                      description="Whether to delete unseen faces", default=True)

    fill_types = [("POSTS", "Posts", "", 0),
                  ("RAILS", "Rails", "", 1), ("WALL", "Wall", "", 2)]
    fill = EnumProperty(description="Type of railing",
                        items=fill_types, default='POSTS')

    def draw(self, context, layout):
        row = layout.row()
        row.prop(self, 'width')

        box = layout.box()
        box.prop(self, 'has_split', toggle=True)
        if self.has_split:
            col = box.column(align=True)
            col.prop(self.split, 'amount', slider=True)

            col = box.column(align=True)
            col.prop(self.split, 'off')

        box = layout.box()
        box.prop(self, 'railing', toggle=True)
        if self.railing:
            row = box.row()
            row.prop(self, "fill", text="")

            col = box.column(align=True)
            if self.fill == 'POSTS':
                col.prop(self, 'pw')
                col.prop(self, 'ph')
                col.prop(self, 'pd')
            elif self.fill == 'RAILS':
                col.prop(self, 'rw')
                col.prop(self, 'rh')
                col.prop(self, 'rd')
            elif self.fill == 'WALL':
                col.prop(self, 'ww')
                col.prop(self, 'wh')

                row = box.row()
                row.prop(self, 'df')

            row = box.row()
            row.prop(self, "hcp", toggle=True)
            if self.hcp:
                # box = layout.box()
                col = box.column(align=True)
                col.prop(self, 'cpw')
                col.prop(self, 'cph')


class RailingProperty(bpy.types.PropertyGroup):
    pw = FloatProperty(name="Post Width", description="Width of each post",
                       min=0.01, max=100.0, default=0.15)

    ph = FloatProperty(
        name="Post Height", description="Height of each post", min=0.01, max=100.0, default=0.7)

    pd = FloatProperty(name="Post Desnsity", description="Number of posts along each edge", min=0.0, max=1.0,
                       default=0.9)

    rw = FloatProperty(name="Rail Width", description="Width of each rail",
                       min=0.01, max=100.0, default=0.15)

    rh = FloatProperty(name="Rail Height", description="Height of each rail",
                       min=0.01, max=100.0, default=0.025)

    rd = FloatProperty(name="Rail Desnsity", description="Number of rails over each edge", min=0.0, max=1.0,
                       default=0.2)

    ww = FloatProperty(name="Wall Width", description="Width of each wall",
                       min=0.01, max=100.0, default=0.075)

    wh = FloatProperty(
        name="Wall Height", description="Height of each wall", min=0.01, max=100.0, default=0.7)

    cpw = FloatProperty(name="Corner Post Width", description="Width of each corner post", min=0.01, max=100.0,
                        default=0.15)

    cph = FloatProperty(name="Corner Post Height", description="Height of each corner post", min=0.01, max=100.0,
                        default=0.7)

    hcp = BoolProperty(
        name="Corner Posts", description="Whether the railing has corner posts", default=True)

    df = BoolProperty(name="Delete Faces",
                      description="Whether to delete unseen faces", default=True)

    fill_types = [("POSTS", "Posts", "", 0),
                  ("RAILS", "Rails", "", 1), ("WALL", "Wall", "", 2)]
    fill = EnumProperty(description="Type of railing",
                        items=fill_types, default='POSTS')

    def draw(self, context, layout):

        row = layout.row()
        row.prop(self, "fill", text="")

        box = layout.box()
        col = box.column(align=True)
        if self.fill == 'POSTS':
            col.prop(self, 'pw')
            col.prop(self, 'ph')
            col.prop(self, 'pd')
        elif self.fill == 'RAILS':
            # col.prop(self, 'rw')
            col.prop(self, 'rh')
            col.prop(self, 'rd')
        elif self.fill == 'WALL':
            col.prop(self, 'ww')
            col.prop(self, 'wh')

            row = box.row()
            row.prop(self, 'df')

        row = layout.row()
        row.prop(self, "hcp", toggle=True)
        if self.hcp:
            box = layout.box()
            col = box.column(align=True)
            col.prop(self, 'cpw')
            col.prop(self, 'cph')


class StairsProperty(bpy.types.PropertyGroup):
    step_count = IntProperty(
        name="Step Count", description="Number of steps", min=1, max=100, default=3)

    step_width = FloatProperty(
        name="Step Width", description="Width of each step", min=0.01, max=100.0, default=.5)

    scale = FloatProperty(
        name="Scale", description="Scale of the steps", min=0.0, max=1.0, default=0.0)

    bottom_faces = BoolProperty(
        name="Bottom Faces", description="Wether to delete bottom faces", default=True)

    def draw(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, 'step_count')
        col.prop(self, 'step_width')

        layout.prop(self, 'scale')
        layout.prop(self, 'bottom_faces', toggle=True)


class StaircaseProperty(bpy.types.PropertyGroup):
    # --landing
    # ****************************
    lcount = IntProperty(name='Landing Count', description='Number of landings in the staircase', min=1, max=100,
                         default=3)

    lwidth = FloatProperty(
        name='Landing Width', description='Width of each landing', min=1.0, max=100.0, default=4.0)

    llength = FloatProperty(name='Landing Length', description='Length of each landing', min=1.0, max=100.0,
                            default=2.5)

    lheight = FloatProperty(name='Landing Height', description='Thickness of each landing', min=0.01, max=100.0,
                            default=.25)

    l_offz = FloatProperty(name='Landing Height Offset', description='Height offset of each landing', min=1.0,
                           max=100.0, default=2.0)

    l_offy = FloatProperty(name='Landing Gap Offset', description='Gap between Each landing', min=1.0, max=100.0,
                           default=4.0)

    #       support
    lsp = FloatProperty(name='Landing Support Width', description='Width of each landing support beam', min=0.01,
                        max=100.0, default=.25)

    #       railing
    lpw = FloatProperty(name='Landing Post Width', description='Width of landing posts ', min=0.01, max=100.0,
                        default=.1)

    lph = FloatProperty(name='Landing Post Height', description='Height of landing posts', min=0.01, max=100.0,
                        default=1.0)

    lpd = FloatProperty(name='Landing Post Density', description='Distribution of landing Posts', min=0.0, max=1.0,
                        default=.4)

    lrw = FloatProperty(name='Landing Rail Width', description='Width of landing rails', min=0.01, max=100.0,
                        default=.2)

    lrh = FloatProperty(name='Landing Rail Height', description='Height of each landing rail', min=0.1, max=100.0,
                        default=1.0)

    # -- steps
    # ****************************
    scount = IntProperty(name='Step Count', description='Number of steps between each landing', min=1, max=100,
                         default=5)

    sgap = FloatProperty(name='Step Gap', description='Gap between each staircase step', min=0.0, max=1.0, default=.25,
                         update=update_sgap)

    #       support
    ssc = IntProperty(name='Step Support Count', description='Number of support beams for steps', min=1, max=10,
                      default=2)

    ssw = FloatProperty(name='Step Support Width', description='Width of each step support beam', min=0.01, max=100.0,
                        default=.2)

    #       railing
    sph = FloatProperty(name='Step Post Height',
                        description='Height of step posts', min=0.01, max=100.0, default=1.0)

    spw = FloatProperty(name='Step Post Width',
                        description='Width of step posts', min=0.01, max=100.0, default=0.1)

    srw = FloatProperty(name='Step Rail Width',
                        description='Width of step rails', min=0.01, max=100.0, default=0.15)

    # -- options
    # ****************************
    hls = BoolProperty(name='Landing Support', description='Whether the staircase landings have support beams',
                       default=False)

    hlr = BoolProperty(name='Landing Rails',
                       description='Whether the staircase landings have railing', default=False)

    hss = BoolProperty(
        name='Step Support', description='Whether the staircase steps have support beams', default=False)

    hsr = BoolProperty(
        name='Step Rails', description='Whether the staircase steps have railing', default=False)

    hisr = BoolProperty(name='Inner Step Rails', description='Whether the staircase steps have inner railing',
                        default=True)

    hosr = BoolProperty(name='Outer Step Rails', description='Whether the staircase steps have outer railing',
                        default=True)

    def draw(self, context, layout):
        box = layout.box()

        col = box.column(align=True)
        col.prop(self, 'lcount')
        col.prop(self, 'lwidth')
        col.prop(self, 'llength')
        col.prop(self, 'lheight')

        box.prop(self, 'l_offz')
        box.prop(self, 'l_offy')

        # -- support
        box = layout.box()
        box.prop(self, 'hls')
        if self.hls:
            col = box.column()
            col.prop(self, 'lsp')

        # -- railing
        box = layout.box()
        box.prop(self, 'hlr')
        if self.hlr:
            # -- Posts
            col = box.column(align=True)
            col.prop(self, 'lpw')
            col.prop(self, 'lph')
            col.prop(self, 'lpd')
            # -- Rails
            col = box.column(align=True)
            col.prop(self, 'lrw')
            # col.prop(self, 'lrh')

        # steps
        layout.label('Steps')
        box = layout.box()

        col = box.column(align=True)
        col.prop(self, 'scount')
        col.prop(self, 'sgap')

        # --support
        box = layout.box()
        box.prop(self, 'hss')
        if self.hss:
            col = box.column()
            col.prop(self, 'ssc')
            # col.prop(self, 'ssw')

        # -- railing
        box = layout.box()
        box.prop(self, 'hsr')
        if self.hsr:
            # -- Posts
            col = box.column(align=True)
            col.prop(self, 'spw')
            col.prop(self, 'sph')

            # -- Rails
            col = box.column(align=True)
            col.prop(self, 'srw')

            # -- Rail options
            box.label('Rail Options')
            row = box.row(align=True)
            row.prop(self, 'hisr', toggle=True)
            row.prop(self, 'hosr', toggle=True)


class RoofProperty(bpy.types.PropertyGroup):
    r_types = [
        ("FLAT", "Flat", "", 0),
        ("GABLE", "Gable", "", 1),
    ]
    type = EnumProperty(description="Type of roof",
                        items=r_types, default='FLAT')

    thick = FloatProperty(
        name="Thickness", description="Thickness of roof hangs", min=0.01, max=1000.0, default=.1)

    outset = FloatProperty(
        name="Outset", description="Outset of roof hangs", min=0.01, max=1000.0, default=.1)

    height = FloatProperty(
        name="Height", description="Height of entire roof", min=0.01, max=1000.0, default=1)

    o_types = [("LEFT", "Left", "", 0), ("RIGHT", "Right", "", 1), ]
    orient = EnumProperty(description="Orientation of gable",
                          items=o_types, default='LEFT')


    def draw(self, context, layout):
        layout.prop(self, 'type', text="")

        box = layout.box()
        if self.type == 'FLAT':
            col = box.column()
            col.prop(self, 'thick')
            col.prop(self, 'outset')

        elif self.type == 'GABLE':
            col = box.column()
            col.prop(self, 'thick')
            col.prop(self, 'outset')
            col.prop(self, 'height')

            row = box.row(align=True)
            row.prop(self, 'orient', expand=True)


# =======================================================
#
#           OPERATORS
#
# =======================================================

class BalconyOperator(bpy.types.Operator):
    """ Creates balconies on selected mesh faces """
    bl_idname = "cynthia.add_balcony"
    bl_label = "Add Balcony"
    bl_options = {'REGISTER', 'UNDO'}

    props = PointerProperty(type=BalconyProperty)

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        props = self.props
        sp = props.split

        me = get_edit_mesh()
        bm = bmesh.from_edit_mesh(me)

        make_balcony(props.width, props.railing, props.pw, props.ph, props.pd, props.rw, props.rh, props.rd, props.ww,
                     props.wh, props.cpw, props.cph, props.hcp, props.df, props.fill, sp.amount[
                         0], sp.amount[1],
                     sp.off[0], sp.off[1], sp.off[2], props.has_split)
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}

    def draw(self, context):
        self.props.draw(context, self.layout)


class RailingOperator(bpy.types.Operator):
    """ Create railing on selected mesh edges """
    bl_idname = "cynthia.add_railing"
    bl_label = "Add Railing"
    bl_options = {'REGISTER', 'UNDO'}

    props = PointerProperty(type=RailingProperty)

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        props = self.props

        me = get_edit_mesh()
        bm = bmesh.from_edit_mesh(me)
        make_railing(bm, [e for e in bm.edges if e.select], props.pw, props.ph, props.pd, props.rw, props.rh, props.rd,
                     props.ww, props.wh, props.cpw, props.cph, props.hcp, props.df, props.fill)
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}

    def draw(self, context):
        self.props.draw(context, self.layout)


class StairsOperator(bpy.types.Operator):
    """ Create stairs on selected mesh faces """
    bl_idname = "cynthia.add_stairs"
    bl_label = "Add Stairs"
    bl_options = {'REGISTER', 'UNDO'}

    props = PointerProperty(type=StairsProperty)

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        props = self.props

        make_stairs_type2(props.step_count, props.step_width,
                          props.scale, props.bottom_faces)

        return {'FINISHED'}

    def draw(self, context):
        self.props.draw(context, self.layout)


class StaircaseOperator(bpy.types.Operator):
    """ Create a staircase object """
    bl_idname = "cynthia.add_staircase"
    bl_label = "Add Staircase"
    bl_options = {'REGISTER', 'UNDO'}

    props = PointerProperty(type=StaircaseProperty)

    def execute(self, context):
        props = self.props

        # Create Staircase Object
        obj = make_object('staircase', make_mesh('sc.mesh'))
        bm = bm_from_obj(obj)

        case = make_stair_case(bm, props.lcount, props.lwidth, props.llength, props.lheight, props.l_offz, props.l_offy,
                               props.lsp, props.lpw, props.lph, props.lpd, props.lrw, props.lrh, props.scount,
                               props.sgap, props.ssc, props.ssw, props.sph, props.spw, props.srw, props.hls, props.hlr,
                               props.hss, props.hsr, props.hisr, props.hosr)

        bm_to_obj(case, obj)
        link_obj(obj)

        return {'FINISHED'}

    def draw(self, context):
        self.props.draw(context, self.layout)


class RoofOperator(bpy.types.Operator):
    """ Create roof on selected mesh faces """
    bl_idname = "cynthia.add_roof"
    bl_label = "Add Roof"
    bl_options = {'REGISTER', 'UNDO'}

    props = PointerProperty(type=RoofProperty)

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        props = self.props

        me = get_edit_mesh()
        bm = bmesh.from_edit_mesh(me)

        if props.type == 'FLAT':
            make_flat_roof(bm, props.thick, props.outset)
        elif props.type == 'GABLE':
            make_gable_roof(bm, props.height, props.outset,
                            props.thick, props.orient)
        else:
            make_hip_roof(bm, me, props.hip_amount, props.height, props.hip_region, props.hip_percent, props.outset,
                          props.thick, props.dissolve, props.dissolve_angle)

        bmesh.update_edit_mesh(me, True)
        return {'FINISHED'}

    def draw(self, context):
        self.props.draw(context, self.layout)


class RemovePropertyOperator(bpy.types.Operator):
    """ Create roof on selected mesh faces """
    bl_idname = "cynthia.remove_property"
    bl_label = "Remove Property"
    bl_options = {'REGISTER'}

    def execute(self, context):
        obj = context.object

        # remove property
        idx = obj.property_index
        obj.property_index -= 1
        obj.property_list.remove(idx)

        # Update building
        update_building(self, context)
        context.area.tag_redraw()

        return {'FINISHED'}


# =======================================================
#
#           PANEL UI
#
# =======================================================

class PROP_items(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        sp = layout.split(percentage=.9)
        sp.prop(item, "name", text="", emboss=False, translate=False, icon='SNAP_PEEL_OBJECT')
        sp.operator("cynthia.remove_property", text="", emboss=False, icon="X")

    def invoke(self, context, event):
        pass


class CynthiaPanel(bpy.types.Panel):
    """Docstring of CynthiaPanel"""
    bl_idname = "VIEW3D_PT_cynthia"
    bl_label = "Cynthia Building Tools"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Cynthia Tools'

    def draw(self, context):
        layout = self.layout
        active = context.object

        # Draw the operators
        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator("cynthia.add_floorplan")
        row.operator("cynthia.add_floors")

        row = col.row(align=True)
        row.operator("cynthia.add_window")
        row.operator("cynthia.add_door")

        row = col.row(align=True)
        row.operator("cynthia.add_balcony")
        row.operator("cynthia.add_railing")

        col.operator("cynthia.add_stairs")
        # col.operator("cynthia.add_staircase")

        col.operator("cynthia.add_roof")

        # Draw Properties
        col = layout.column(align=True)
        col.box().label("Properties")

        if active:
            box = col.box()
            obj = context.object

            # Draw UIlist for all property groups
            rows = 2
            row = box.row()
            row.template_list("PROP_items", "", obj, "property_list", obj, "property_index", rows=rows)


            # draw  properties for active group
            active_index = obj.property_index
            if not len(obj.property_list):
                return
            active_prop = obj.property_list[active_index]

            if active_prop.type     == 'FLOORPLAN':
                fp_props = obj.building.floorplan
                fp_props.draw(context, box)
            elif active_prop.type   == 'FLOOR':
                floor_props = obj.building.floors
                floor_props.draw(context, box)
            elif active_prop.type   == 'WINDOW':
                win_prop = obj.building.windows[active_prop.id]
                win_prop.draw(context, box)
            elif active_prop.type   == 'DOOR':
                door_prop = obj.building.doors[active_prop.id]
                door_prop.draw(context, box)


# =======================================================
#
#           REGISTER
#
# =======================================================

def register():
    register_core()


def unregister():
    unregister_core()

if __name__ == "__main__":
    import os
    os.system("clear")
    # useful for continuous updates
    try:
        unregister()
    except Exception as e:
        import traceback; traceback.print_exc()
        print("UNREGISTERED MODULE .. FAIL", e)
    register()


    # # optional run tests
    # from .tests import CynthiaTest
    # CynthiaTest.run_tests()

    # Dev --init workspace
    # --clear
    # bpy.ops.object.select_all(action="SELECT")
    # bpy.ops.object.delete(use_global=False)
    # for mat in bpy.data.materials:
    #     bpy.data.materials.remove(mat)
    # # -- add
    # bpy.ops.cynthia.add_floorplan()
    # bpy.ops.cynthia.add_floors()
    # bpy.context.object.building.floors.floor_count = 3
    # bpy.context.object.building.floors.floor_height = 3
