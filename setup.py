from setuptools import setup, find_packages

setup(
    name="pwm",
    version="0.1",
    packages=find_packages(),
    scripts=["pwm.py"],
    install_requires=["cffi"],
    include_package_data=True,
    test_suite="test",

    author="Michael Bitzi",
    author_email="mibitzi@gmail.com",
    description="A simplistic tiling window manager",
    license="MIT",
    keywords="pwm tiling window manager",
    url="https://github.com/mibitzi/pwm"
)
