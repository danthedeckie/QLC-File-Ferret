# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['I:\\Public Ministries\\AV Team\\07 - Projects\\2019 - DF - QLC File Fixer'],
             binaries=[],
             datas=[('icons\\', 'icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='QLC-file-ferret',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          onefile=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='QLC-file-ferret')
