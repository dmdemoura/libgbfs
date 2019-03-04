# GBFS
### A read-only filesystem for game media in Game Boy Advance roms by Damian Yerrick

Ever wanted to include media (images, palettes, sound samples, etc.)
in GBA games?  Tired of repeatedly converting your binary media
files to source code and having to give your artists copies of
your compiler toolchain to test their work in an emulator?
Here's another solution.

GBFS is an archive format.  It is similar in principle to GNU 'tar'
but is much simpler in structure, has an order of magnitude less
overhead per stored object (32 bytes vs. 500 bytes), and can be
searched in O(log n) time rather than O(n) time.

GBFS comes with four utility programs for the host system and a small
library for the target system for accessing GBFS files.

---
### About this repository
This is repository contains libgbfs release 20060815, repackaged as a CMake project, configured to be able installed and let other CMake projects include it using find_package(libgbfs).
It does not include the GBFS tools, only the library. For the tools use devkitpro, or get the original package from [the official site](https://pineight.com/gba/#gbfs).
This repository is not affiliated with Damian Yerrick. 

---
###  Library function calls

The file `libgbfs.c`, licensed under a simple permissive license,
implements the following functions.  Use `gbfs.h` to get their
prototypes.

### `const GBFS_FILE *find_first_gbfs_file(const void *start);`
  Finds the first GBFS file after start.  Note that this does a
  slow linear search at 256-byte strides, so make sure that your
  files are aligned to 256-byte boundaries and that you pass a start
  location close to (but not past) the beginning of the GBFS file.
  
  If you concatenate the GBFS file immediately after the binary, and
  `libgbfs.c` appears near the end of the link order, you can do this
  cute trick to find a file:  `find_first_gbfs_file(find_first_gbfs_file);`

### `const void *skip_gbfs_file(const GBFS_FILE *file);`
  Returns the address of the end of the given GBFS file.  This is
  useful if you want to have more than one GBFS file in a single
  binary, such as if you have multiple musicians and artists
  working on their own parts of a project.

### `const void *gbfs_get_obj(const GBFS_FILE *file, const char *name, unsigned int *len);`
  Performs a binary search inside the given file for an object with
  the given name and returns a pointer to the object.  If `len` is not
  `NULL`, `gbfs_get_obj()` stores the length of the object (in bytes)
  into the referenced location.  If the object was not found,
  `gbfs_get_obj()` returns `NULL` and does not modify `*len`.
  A search on a file that contains two objects of the same name will
  return an undefined result.  The current implementation of
  `gbfs_get_obj()` uses `bsearch()` from the C library as its backend.

### `size_t gbfs_count_objs(const GBFS_FILE *file);`
  If file is `NULL`, returns 0.  Otherwise, returns the number of
  objects in the given file.

### `const void *gbfs_get_nth_obj(const GBFS_FILE *file, size_t n, char name[], unsigned int *len);`
  Returns a pointer to the (n + 1)th object in the given file.  If
  name is not `NULL`, `gbfs_get_nth_obj()` copies the name of the object
  into the buffer, which must be at least 25 bytes long.  If len is
  not `NULL`, `gbfs_get_nth_obj()` stores the length of the object (in
  bytes) into the referenced location.  If `n` is greater than or equal
  to the number of objects in the file, `gbfs_get_nth_obj()` returns
  `NULL` and does not modify `*len` or `name[]`.

### `void *gbfs_copy_obj(void *dst, const GBFS_FILE *file, const char *name);`
  Calls `gbfs_get_obj()` to find an object with the given name, copies
  it to memory starting at `dst[0]` using `memcpy()`, and returns `dst`.
  If the object was not found, `gbfs_copy_obj()` returns `NULL` and does
  not modify memory.  Hint: for speed, override `memcpy()` with a DMA
  copy on platforms that support it.

---
`gbfs_get_nth_obj()` and `gbfs_copy_obj()` have not been tested as
rigorously as the rest of the library.

---
###  GBFS file format

Integers are stored in little-endian byte order because that's what
the local scene's favorite machines (SNES, GBA, PC) tend to use.

typedef struct GBFS_FILE
{
  char magic[16];    /* "PinEightGBFS\r\n\032\n" */
  u32  total_len;    /* total length of archive */
  u16  dir_off;      /* offset in bytes to directory */
  u16  dir_nmemb;    /* number of files */
  char reserved[8];  /* for future use */
} GBFS_FILE;

typedef struct GBFS_ENTRY
{
  char name[24];     /* filename, nul-padded */
  u32  len;          /* length of object in bytes */
  u32  data_offset;  /* in bytes from beginning of file */
} GBFS_ENTRY;

Note that GBFS_ENTRY records must be sorted in memcmp() order
by name so that the binary search can do its job correctly.

### Change log
#### 20060815
 * Updates the sample program's build script for devkitARM R19b. 
 * Increases the number of files that can be put into a GBFS archive
 * Adds notes in the manual about issues related to the Nintendo DS.

#### 20040208
  * sped up find_first_gbfs_file() for multiboot programs that read
    GBFS files in ROM; now the search skips 0x02040000 to 0x08000000,
    speeding up DKA R5b3 multiboot programs' searches
  * changed to fix a compilation problem on a Mac compiler
    (reported by Jason Kim <jmkim@uci.edu>)
  * added gbfs_copy_obj() to make it easier to dump graphics to VRAM
  * added gbfs_count_objs() and gbfs_get_nth_obj()
  * included bin2s so that GBFS archives can be compiled to .elf
    for debugging support
  * replaced DOS executables with Windows ones because so many of us
    have moved on to Windows 2000 and XP

#### 20030121
  * added exception to the tools' licenses to allow them to be
    used in Photoshop plug-ins
  * clarified license of manual
  * fixed warnings about missing strcmp() prototype
  * worked around MinGW's fclose(NULL) behavior, which crashes
    instead of doing nothing
  * recompiled the included binaries with a more recent version
    of MinGW
  * changed padbin.exe to pad with 0xff instead of 0x00 for faster
    flash writing
  * added a compile time option to libgbfs.c to make
    find_first_gbfs_file() use an alignment of any power of 2.
    I normally use a 256-byte alignment, which provides a
    reasonably fast search of the 32 MB cart address space.

#### 20020404
  * changed upper bound on find_first_gbfs_file() in libgbfs.c
    to the end of ROM rather than the end of EWRAM to make libgbfs
    compatible with ROM-based programs
  * Added skip_gbfs_file() to find the end of a GBFS file
  * Clarified license of gbfs.h

#### 20020402
  * Initial release
  
  ---
### Legal

Copyright 2002-2003 Damian Yerrick.
This manual (but not the accompanying programs) is subject to the
QING PUBLIC LICENCE

Copying, distribution, public performance, public display, digital
audio transmission, and use of this work is permitted without
restriction.  Circumvention of any technological measure or measures
which effectively control access to this work is permitted without
restriction.  Preparation of derivative works is permitted provided
that you cause any such work to be licensed as a whole at no charge
to all third parties under the terms of this License.

The programs in this package are released under their own licenses;
check the source code files for details.