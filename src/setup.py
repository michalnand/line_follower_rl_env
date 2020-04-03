from setuptools import setup
 
setup(  name="gym_linefollower", 
        version="1.0",
        author="Michal Chovanec",
        license="MIT",
        include_package_data=True,
        nstall_requires=["gym", "numpy", "pybullet", "opencv-python", "shapely"])

