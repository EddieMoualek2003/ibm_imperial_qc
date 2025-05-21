# import os
# import sys

# # Step 1: Automatically add the parent directory to sys.path
# # This allows absolute imports to work
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)

# if project_root not in sys.path:
#     sys.path.insert(1, project_root)

# # Step 2: Now do the absolute import
# from IBM_QC_Integrated_Platform.lights_out.lights_out_top import lights_out_main

from lights_out_top import *

# Step 3: Main entry
if __name__ == "__main__":
    lights_out_main()
