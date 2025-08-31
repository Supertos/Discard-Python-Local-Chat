'''
Discard - instant messaging application.

See `README.md` in the project root for full descripton.
'''

try:
    from importlib.metadata import version
    __version__ = version("discard")
except ImportError:
    __version__ = "0.0.0"
