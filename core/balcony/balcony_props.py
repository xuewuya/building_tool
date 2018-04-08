import bpy
from bpy.props import *

from ..generic import SplitProperty

class BalconyProperty(bpy.types.PropertyGroup):
    width   = FloatProperty(
        name="Balcony Width", min=0.01, max=100.0, default=2,
        description="Width of balcony")

    railing = BoolProperty(
        name="Add Railing", default=True,
        description="Whether the balcony has railing")

    pw = FloatProperty(
        name="Post Width", min=0.01, max=100.0, default=0.15,
        description="Width of each post")

    ph = FloatProperty(
        name="Post Height", min=0.01, max=100.0, default=0.7,
        description="Height of each post")

    pd = FloatProperty(
        name="Post Desnsity", min=0.0, max=1.0,default=0.9,
        description="Number of posts along each edge")

    rw = FloatProperty(
        name="Rail Width", min=0.01, max=100.0, default=0.15,
        description="Width of each rail")

    rh = FloatProperty(
        name="Rail Height",
        description="Height of each rail",
                       min=0.01, max=100.0, default=0.025)

    rd = FloatProperty(
        name="Rail Desnsity", min=0.0, max=1.0,default=0.2,
        description="Number of rails over each edge")

    ww = FloatProperty(
        name="Wall Width", min=0.01, max=100.0, default=0.075,
        description="Width of each wall")

    wh = FloatProperty(
        name="Wall Height", min=0.01, max=100.0, default=0.7,
        description="Height of each wall")

    cpw = FloatProperty(
        name="Corner Post Width", min=0.01, max=100.0, default=0.15,
        description="Width of each corner post")

    cph = FloatProperty(
        name="Corner Post Height", min=0.01, max=100.0, default=0.7,
        description="Height of each corner post")

    hcp = BoolProperty(
        name="Corner Posts", default=True,
        description="Whether the railing has corner posts")

    df = BoolProperty(
        name="Delete Faces", default=True,
        description="Whether to delete unseen faces")

    fill_types = [("POSTS", "Posts", "", 0),
                  ("RAILS", "Rails", "", 1), ("WALL", "Wall", "", 2)]
    fill = EnumProperty(
        items=fill_types, default='POSTS',
        description="Type of railing")

    has_split = BoolProperty(
        name="Add Split", default=False,
        description="Whether to split the balcony face")

    split = PointerProperty(type=SplitProperty)

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
