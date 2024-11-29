# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_data_files
import os

base_path = 'C:\\Users\\karim\\Documents\\studia_materialy\\semestr_7\\game3'

ursina_path = os.path.join(base_path, 'venv\\Lib\\site-packages\\ursina')
ursina_dist_info_path = os.path.join(base_path, 'venv\\Lib\\site-packages\\ursina-7.0.0.dist-info')

panda3d_path = os.path.join(base_path, 'venv\\Lib\\site-packages\\panda3d')
panda3d_tools_path = os.path.join(base_path, 'venv\\Lib\\site-packages\\panda3d_tools')
panda3d_dist_info_path = os.path.join(base_path, 'venv\\Lib\\site-packages\\panda3d-1.10.14.dist-info')

datas, binaries, hiddenimports = collect_all('ursina')

mtcnn_datas = collect_data_files('mtcnn')

datas += mtcnn_datas + [
#    (os.path.join(base_path, 'assets'), 'assets'),
    (os.path.join(base_path, 'config'), 'config'),
    (os.path.join(base_path, 'player_data'), 'player_data'),
#    (os.path.join(base_path, 'models_compressed'), 'models_compressed'),
    (os.path.join(base_path, 'models.mf'), 'models.mf'),
    (ursina_path, 'ursina'),
    (ursina_dist_info_path, 'ursina-7.0.0.dist-info'),
    (panda3d_path, 'panda3d'),
    (panda3d_tools_path, 'panda3d_tools'),
    (panda3d_dist_info_path, 'panda3d-1.10.14.dist-info')
]

a = Analysis(
    ['game.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='game',
)





