cmake_minimum_required(VERSION 3.5)
project(GBFS VERSION 2006.08.15 LANGUAGES C)

set(CPACK_PACKAGE_NAME libgbfs)
set(CPACK_PACKAGE_VENDOR placeholder)
set(CPACK_PACKAGE_CONTACT placeholder)

include(CPack)
include(GNUInstallDirs)

add_library(libgbfs source/libgbfs.c)
set_target_properties(libgbfs PROPERTIES PREFIX "") #So we don't end up with liblibgbfs
target_include_directories(libgbfs
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

#For instalation of static library files.
install(TARGETS libgbfs
    EXPORT libgbfs-config
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
#For instalation of include files.
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
#For installation of CMake config files. For find_package().
install(EXPORT libgbfs-config DESTINATION ${CMAKE_INSTALL_DATADIR}/libgbfs)
