cmake_minimum_required(VERSION 3.5)
project(GBFS VERSION 2006.08.15 LANGUAGES C)

execute_process(COMMAND echo ${CMAKE_SOURCE_DIR})
execute_process(COMMAND python3 ${BUILDSYSTEM_ROOT}/findSources.py -l sources -e .c source include -o ${CMAKE_BINARY_DIR}/sources.cmake WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

set(CPACK_PACKAGE_NAME libgbfs)
set(CPACK_PACKAGE_VENDOR Demoura)
set(CPACK_PACKAGE_CONTACT gdeperes@gmail.com)

include(${BUILDSYSTEM_ROOT}/GBA.cmake)
include(${CMAKE_BINARY_DIR}/sources.cmake)
include(CPack)

add_library(libgbfs ${sources})
set_target_properties(libgbfs PROPERTIES PREFIX "")
target_include_directories(libgbfs
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

include(GNUInstallDirs)
install(TARGETS libgbfs
    EXPORT gbfs-config
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT gbfs-config DESTINATION ${CMAKE_INSTALL_DATADIR}/libgbfs)
