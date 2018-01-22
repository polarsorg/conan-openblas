#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from glob import glob
import os


class openblasConan(ConanFile):
    name = "openblas"
    version = "0.2.20"
    url = "https://github.com/xianyi/OpenBLAS"
    homepage = "http://www.openblas.net/"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."
    license = "BSD 3-Clause"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "use_mass": [True, False],
               "use_openmp": [True, False],
               "no_lapacke": [True, False]
              }
    default_options = "shared=True", "use_mass=False", "use_openmp=False", "no_lapacke=False"

    def get_make_arch(self):
        return "32" if self.settings.arch == "x86" else "64"

    def get_make_build_type_debug(self):
        return "0" if self.settings.build_type == "Release" else "1"

    def get_make_option_value(self, option):
        return "1" if option else "0"

    def configure(self):
        if self.settings.compiler != "Visual Studio" and self.options["shared"]:
            raise Exception("Shared build only supported in Visual Studio: "
                            "https://github.com/xianyi/OpenBLAS/blob/v0.2.20/CMakeLists.txt#L177")

    def source(self):
        source_url = "https://sourceforge.net/projects/openblas"
        file_name = ("{0} {1} version".format("OpenBLAS", self.version))
        tools.get("{0}/files/v{1}/{2}.tar.gz".format(source_url, self.version, file_name))
        os.rename(glob("xianyi-OpenBLAS-*")[0], "sources")

    def build(self):
        make_program = os.getenv("CONAN_MAKE_PROGRAM", "make")

        if tools.which(make_program):
            make_options = "DEBUG={0} NO_SHARED={1} BINARY={2} NO_LAPACKE={3} USE_MASS={4} USE_OPENMP={5}".format(
                self.get_make_build_type_debug(),
                self.get_make_option_value(self.options.shared),
                self.get_make_arch(),
                self.get_make_option_value(self.options.no_lapacke),
                self.get_make_option_value(self.options.use_mass),
                self.get_make_option_value(self.options.use_openmp))
            self.run("cd sources && make %s" % make_options)
        else:
            cmake = CMake(self)
            cmake.configure(source_dir="sources")
            cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE", dst="licenses", src="sources",
                      ignore_case=True, keep_path=False)

            if self.settings.compiler == "Visual Studio":
                self.copy(pattern="*.h", dst="include", src=".")
            else:
                self.copy(pattern="*.h", dst="include", src="sources")

            self.copy(pattern="*.dll", dst="bin", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Linux" and not self.options["shared"]:
            self.cpp_info.libs.append("pthread")
