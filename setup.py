
from setuptools import setup

setup(
    name="pywebp-gtk",
    version="0.0.1.dev0",
    packages=['pywebp'],
    scripts=['pywebp/pywebp'],
    install_requires=['PyGObject'],
    description="A converter for WebP image format",
    license="MIT",
    url="https://github.com/tudo75/PyWebP-Gtk",
)
