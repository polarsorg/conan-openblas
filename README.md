# conan-openblas

![conan-openblas image](/images/conan-openblas.png)

[![Download](null/packages/conan-community/conan/openblas%3Aconan/images/download.svg?version=0.2.20%3Astable)](https://bintray.com/conan-community/conan/openblas%3Aconan/0.2.20%3Astable/link)
[![Build Status](https://travis-ci.org/danimtb/conan-openblas.svg?branch=stable%2F0.2.20)](https://travis-ci.org/danimtb/conan-openblas)
[![Build status](https://ci.appveyor.com/api/projects/status/hj182uagiarwi8mb/branch/stable/0.2.20?svg=true)](https://ci.appveyor.com/project/danimtb/conan-openblas/branch/stable/0.2.20)

[Conan.io](https://conan.io) package for [OpenBLAS](https://github.com/xianyi/OpenBLAS) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/conan-community/conan/openblas%3Aconan).

## For Users: Use this package

### Basic setup

    $ conan install OpenBLAS/0.2.20@conan/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    OpenBLAS/0.2.20@conan/stable

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

**Note:** It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to `danimtb` conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from `build_requires` and `requires` , and then running the `build()` method.

    $ conan create conan/stable

## Add Remote

    $ conan remote add conan-community "https://api.bintray.com/conan/conan-community/conan"

## Upload

    $ conan upload OpenBLAS/0.2.20@conan/stable --all -r conan-community

## License

[MIT License](LICENSE)
