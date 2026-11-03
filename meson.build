python_mod = import('python')
py = python_mod.find_installation('python3', required: false)

pypole_sources = files(
  'pypole/__init__.py',
  'pypole/client.py',
  'pypole/errors.py',
  'pypole/robot.py',
  'pypole/turtle.py',
)

# 1. Install to standard Python site-packages/purelib if Python is available
if py.found()
  py.install_sources(
    pypole_sources,
    subdir: 'pypole',
  )
  py.install_sources(
    pypole_sources,
    subdir: 'pole',
  )
endif

# 2. Also install into Pole private data directory for embedded runtime execution
# so Pole can execute Python scripts without depending on host OS site-packages
install_data(
  pypole_sources,
  install_dir: datadir / 'pole' / 'python' / 'pypole',
)
install_data(
  pypole_sources,
  install_dir: datadir / 'pole' / 'python' / 'pole',
)
