#
#  MIT License
#
#  Copyright (c) 2020-2021 Nicola Tudino aka tudo75
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#
# Makefile for the project


# help command for makefile, put here so that "make" without argument is like "make help".
help:
	@echo "-------------------------HELP--------------------------"
	@echo "To build project documentation type make pywebp-docs"
	@echo "To run project tests type make pywebp-tests"
	@echo "To build exe in one dir type make pywebp-build"
	@echo "To build single file exe type make pywebp-build-onefile"
	@echo "-------------------------------------------------------"

# build documentation in the docs folder using sphinx
pywebp-docs:
	cd docs && $(MAKE) html

# Execute tests with pytest
pywebp-tests:
	pytest tests

# build exe for windows in a single folder structure
pywebp-build:
	pyinstaller.exe pywebp.spec

# build single file exe
pywebp-build-onefile:
#	pyinstaller.exe --windowed --clean --onefile --add-data "pywebp/images;pywebp/images" --name pywebp-onefile --debug all --noupx --icon pywebp/images/Icon.ico pywebp-main.pyw
	pyinstaller.exe pywebp-onefile.spec