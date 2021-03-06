import os
import shutil
from conans import ConanFile, CMake, tools


class ParsonConan(ConanFile):
    name = "parson"
    version = "0.1.0"
    homepage = "https://github.com/kgabis/parson"
    url = "https://github.com/bincrafters/conan-parson"
    description = "Lightweight JSON library written in C."
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    _source_subfolder = "source_subfolder"

    def source(self):
        commit = "4f3eaa6849ba62404fc5756650168bb2056d0b46"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, commit))
        extracted_dir = self.name + "-" + commit
        os.rename(extracted_dir, self._source_subfolder)
        shutil.move("CMakeLists.txt", self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
