set(CMAKE_SYSTEM_NAME GBA)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(devkitarm $ENV{DEVKITARM})
set(prefix ${devkitarm}/bin/arm-none-eabi-)

set(CMAKE_C_COMPILER ${prefix}gcc)
set(CMAKE_CXX_COMPILER ${prefix}g++)
set(CMAKE_ASM_COMPILER ${prefix}gcc)
set(CMAKE_OBJCOPY ${prefix}objcopy)

set(ASM_OPTIONS "-x assembler-with-cpp")
set(CMAKE_ASM_FLAGS "${CFLAGS} ${ASM_OPTIONS}")

function(add_rom target)
    message(${target})
    add_executable(${target}.elf EXCLUDE_FROM_ALL source/main.c)
    set_target_properties(${target}.elf PROPERTIES COMPILE_OPTIONS -specs=gba.specs)
    set_target_properties(${target}.elf PROPERTIES LINK_FLAGS -specs=gba.specs)

    add_custom_command(
        OUTPUT ${target}.bin
        MAIN_DEPENDENCY ${target}.elf
        COMMENT "Striping Binary"
        COMMAND ${CMAKE_OBJCOPY} -O binary ${target}.elf ${target}.bin
    )
    add_custom_command(
        OUTPUT ${target}.gba
        MAIN_DEPENDENCY ${target}.bin
        COMMENT "Fixing ROM"
        COMMAND cp ${target}.bin ${target}.gba && gbafix ${target}.gba
    )
    add_custom_target(
        cpong
        ALL
        COMMENT "Building ${target}"
        DEPENDS ${target}.gba
    )
endfunction()