#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from glob import glob
import os


class OpenBLASConan(ConanFile):
    name = "OpenBLAS"
    version = "0.2.20"
    url = "https://github.com/xianyi/OpenBLAS"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."
    license = "https://github.com/xianyi/OpenBLAS/blob/master/LICENSE"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"NO_SHARED": ["1", "0"],
               "cmake": [True, False],
               "USE_MASS": ["1", "0"],  # Compile with MASS Support on Power CPU (Optional dependency)
               "USE_OPENMP": ["1", "0"],
               "NO_LAPACKE": ["1", "0"]
              }
    default_options = "NO_SHARED=0", "cmake=False", "USE_MASS=0", "USE_OPENMP=0", "NO_LAPACKE=0"

    def get_make_arch(self):
        if self.settings.arch == "x86":
            return "32"
        else:
            return "64"

    def get_make_build_type_debug(self):
        if self.settings.build_type == "Release":
            return "0"
        else:
            return "1"

    def source(self):
        source_url = "https://sourceforge.net/projects/openblas"
        file_name = ("{0} {1} version".format(self.name, self.version))
        tools.get("{0}/files/v{1}/{2}.tar.gz".format(source_url, self.version, file_name))
        os.rename(glob("xianyi-OpenBLAS-*")[0], "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        if self.options.cmake or self.settings.compiler == "Visual Studio":
            cmake = CMake(self)
            cmake.configure(source_dir="sources")
            cmake.build()
        else:
            make_options = "DEBUG={0} NO_SHARED={1} BINARY={2} NO_LAPACKE={3} USE_MASS={4} USE_OPENMP={5}".format(self.get_make_build_type_debug(), self.options.NO_SHARED, self.get_make_arch(), self.options.NO_LAPACKE, self.options.USE_MASS, self.options.USE_OPENMP)
            self.run("cd sources && make %s" % make_options)

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")

            if self.settings.compiler == "Visual Studio":
                self.copy(pattern="*.h", dst="include", src=".")
            else:
                self.copy(pattern="*.h", dst="include", src="sources")
            self.copy(pattern="*.dll", dst="bin", src="lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
