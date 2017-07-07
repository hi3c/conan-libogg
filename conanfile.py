from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os
import platform


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    ios_archs = ("arm64", "armv7", "x86_64", "i386")
    requires = "multibuilder/1.0@hi3c/experimental"

    def source(self):
        tools.download("http://www.zlib.net/zlib-1.2.11.tar.gz", "zlib.tar.gz")
        tools.unzip("zlib.tar.gz")
        os.remove("zlib.tar.gz")

    def real_build(self, arch, triple=None):
        atbe = AutoToolsBuildEnvironment(self)
        atbe.fpic = True
        atbe.configure(configure_dir=os.path.join(self.conanfile_directory, "zlib-1.2.11"),
            build=False, host=False, target=False)
        atbe.make()

    def build(self):
        if self.settings.arch == "universal":
            with tools.pythonpath(self):
                from multibuilder import MultiBuilder
                self.builder = MultiBuilder(self, self.ios_archs)
                self.builder.multi_build(self.real_build)
           
    def package(self):
        self.copy("*.h", dst="include", src="zlib-1.2.11")
        self.copy("*.lib", dst="lib", src="build-universal", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", dst="bin", src="build-universal", keep_path=False)
            self.copy("*.so", dst="lib", src="build-universal", keep_path=False)
            self.copy("*.dylib", dst="lib", src="build-universal", keep_path=False)
        else:
            self.copy("*.a", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["z"]
