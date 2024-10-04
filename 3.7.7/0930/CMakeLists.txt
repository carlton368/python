cmake_minimum_required(VERSION 3.10)

set(PROJECT_NAME "Python3.7")
project(${PROJECT_NAME})

include(ExternalProject)

set(EXT_PROJECT_NAME "Python")
set(EXT_PROJECT_URL "https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz")
set(EXT_PROJECT_HASH "SHA256=8c8be91cd2648a1a0c251f04ea0bb4c2a5570feb9c45eaaa2241c785585b475a")

set(ADDITIONAL_CONFIGURE_ARGS 
    --enable-shared
    --with-ensurepip=install
)

ExternalProject_Add(${EXT_PROJECT_NAME}
    URL ${EXT_PROJECT_URL}
    URL_HASH ${EXT_PROJECT_HASH}
    CONFIGURE_COMMAND <SOURCE_DIR>/configure --prefix=${CMAKE_INSTALL_PREFIX} ${ADDITIONAL_CONFIGURE_ARGS}
    BUILD_COMMAND make
    INSTALL_COMMAND make install
    BUILD_IN_SOURCE 1
    LOG_DOWNLOAD ON
    LOG_CONFIGURE ON
    LOG_BUILD ON
    LOG_INSTALL ON
)

# Add custom target for installation
add_custom_target(install_python
    DEPENDS ${EXT_PROJECT_NAME}
    COMMAND ${CMAKE_COMMAND} -E echo "Installing Python..."
    COMMAND ${CMAKE_COMMAND} --build . --target ${EXT_PROJECT_NAME}
    COMMAND ${CMAKE_COMMAND} -E echo "Python installation complete."
)

set(BUILD_SHARED_LIBS ON CACHE BOOL "Build shared libraries")
