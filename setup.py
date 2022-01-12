from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in rfq_sign/__init__.py
from rfq_sign import __version__ as version

setup(
	name="rfq_sign",
	version=version,
	description="Make user\'s default email signature to appear in rfq email",
	author="Ro",
	author_email="roshna@craftinteractive.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
