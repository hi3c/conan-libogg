from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class LiboggConan(ConanFile):
    name = "libogg"
    version = "1.3.2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        tools.download("http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz", "libogg.tar.gz")
        tools.unzip("libogg.tar.gz")
        os.remove("libogg.tar.gz")

    def build(self):
        atbe = AutoToolsBuildEnvironment(self)
        atbe.configure(configure_dir="libogg-1.3.2", args=["--with-pic"])
        atbe.make()

    def package(self):
        self.copy("*.h", dst="include", src="libogg-1.3.2/include")
        self.copy("*.lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ogg"]
