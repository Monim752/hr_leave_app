from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="hr_leave",
    version="0.0.1",
    description="HR Leave & Attendance Module",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Monim",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
