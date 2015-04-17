
from setuptools import setup, find_packages

setup(

    name = "AXUI",
    packages = find_packages(),
    package_data = {"AXUI":["global.cfg"], "AXUI.XML":["schemas/AXUI_app_map.xsd"], "AXUI.driver.windows":["screenshot/screenshot.exe"]},
    version = "0.1.5",
    description = "UI auto framework",
    author = "xcgspring",
    author_email = "xcgspring@163.com",
    license = "Apache Licence Version 2.0",
    url = "https://github.com/xcgspring/AXUI",
    download_url = "",
    keywords = ["UI", "auto"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        ],
    long_description = ''' '''
    
)
