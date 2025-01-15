#!/usr/bin/env python3
import sys
import traceback

try:
    import xr_startmain
except Exception as e:
    print("Error importing xr_startmain:")
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    xr_startmain.main()
except Exception as e:
    print("Error running main:")
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1) 