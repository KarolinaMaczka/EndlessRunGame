from panda3d.core import SamplerState, Multifile, VirtualFileSystem
from ursina import Texture


class Models:

    def __init__(self, app):
        self.app = app

        self.train = app.loader.loadModel('./models_compressed/Train_exp.bam')
        tex = Texture(app.loader.loadTexture('./models_compressed/Train.png'))
        tex._cached_image = None
        self.train_tex = tex

        tex = Texture('./models_compressed/Texture_Col.png', filtering='default')
        tex._cached_image = None
        self.cube = app.loader.loadModel('./models_compressed/Cube.bam')
        self.cube_tex = tex

        tex = Texture(app.loader.loadTexture('./models_compressed/madera-textura.jpg'))
        tex._cached_image = None
        mod = app.loader.loadModel('./models_compressed/fence.bam')
        self.fence = mod
        self.fence_tex = tex

        tex = Texture(app.loader.loadTexture('./models_compressed/wood_text.png'))
        tex._cached_image = None
        mod = app.loader.loadModel('./models_compressed/Sign.bam')
        self.wood_sign = mod
        self.wood_sign_tex = tex

        tex = Texture(app.loader.loadTexture('./models_compressed/container.jpg'))
        tex._cached_image = None
        mod = app.loader.loadModel('./models_compressed/objStairs.bam')
        self.container = mod
        self.container_tex = tex

        tex = Texture(app.loader.loadTexture('./models_compressed/wood_text.png'))
        tex._cached_image = None
        self.gate_tex = tex

        tex = app.loader.loadTexture('./models_compressed/pole.png')
        tex.setWrapU(SamplerState.WM_clamp)
        tex.setWrapV(SamplerState.WM_clamp)
        tex = Texture(tex)
        tex._cached_image = None
        self.pole_tex = tex

        mod = app.loader.loadModel('./models_compressed/indicater2.bam')
        self.indicator = mod

        mod = app.loader.loadModel('./models_compressed/cube_obj.bam')
        self.cube_standard = mod

        # trnasformations
        # tex = Texture('assets/container2/Texture_Col.png', filtering='default')
        # tex._cached_image = None
        # m = mesh_importer.obj_to_ursinamesh(name='Cube', return_mesh=True)
        # m.path = None
        # m.name = 'Cube'
        # mesh_importer.imported_meshes['Cube'] = m
        # m.save(f'Cube.bam')
        # mod = app.loader.loadModel('./models_compressed/Cube.bam')


