# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['alien_invision.py'],
    pathex=['C:/Users/Ray/PycharmProjects/alien_invasion'],
    binaries=[],
    datas=[('images/alien.png', 'images'),
    ('images/ship.png', 'images'),
    ('images/ship_left.png', 'images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='alien_invision',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = 'C:/Users/Ray/PycharmProjects/alien_invasion/images/icon.ico'
)
