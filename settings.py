"""
Global settings for PRS design directory builder.
"""

STAGES = ("setup",
          "rtlscr",
          "cstr",
          "pcstr",
          "ultra",
          "tcstr",
          "icstr",
          "incr",
          "post")


PREFIX_TECH_FILES = "lib_data/rcxt"

PREFIX_USER_DATA = "<product>_user_data"

PREFIX_OTHER_SCRIPTS = "<product>_user_data/CONSTRAINT/scripts"
