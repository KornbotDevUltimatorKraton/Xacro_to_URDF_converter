import os
import sys
import types
import xacro

# Base directory where this script and files reside
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Candidate directories where the ROS package 'Bipedal_robotics_part_v2_description' may be located
CANDIDATE_PACKAGE_DIRS = [
    r"C:\Users\Kornbotdev\Desktop\URDDF_export\Bipedal_robotics_part_v2_description",
    os.path.join(BASE_DIR, "Bipedal_robotics_part_v2_description"),
    BASE_DIR,
]

def resolve_package_dir(pkg_name):
    for candidate in CANDIDATE_PACKAGE_DIRS:
        if os.path.isdir(candidate):
            # Check if this candidate contains the expected 'urdf' folder or xacro files
            if os.path.exists(os.path.join(candidate, "urdf", "materials.xacro")) or \
               os.path.exists(os.path.join(candidate, "materials.xacro")):
                return candidate
    return BASE_DIR

PACKAGE_FOLDER = resolve_package_dir("Bipedal_robotics_part_v2_description")

# 1. Mock 'ament_index_python' for ROS 2 style $(find ...)
ament_mod = types.ModuleType("ament_index_python")
packages_mod = types.ModuleType("ament_index_python.packages")
packages_mod.get_package_share_directory = lambda pkg: PACKAGE_FOLDER
ament_mod.packages = packages_mod
sys.modules["ament_index_python"] = ament_mod
sys.modules["ament_index_python.packages"] = packages_mod

# 2. Mock 'rospkg' for ROS 1 style $(find ...)
rospkg_mod = types.ModuleType("rospkg")
class MockRosPack:
    def get_path(self, pkg):
        return PACKAGE_FOLDER
rospkg_mod.RosPack = MockRosPack
sys.modules["rospkg"] = rospkg_mod

def convert_xacro_to_urdf():
    # Locate input xacro file
    input_xacro = os.path.join(BASE_DIR, "Bipedal_robotics_part_v2.xacro")
    if not os.path.exists(input_xacro):
        alt_input = os.path.join(BASE_DIR, "urdf", "Bipedal_robotics_part_v2.xacro")
        if os.path.exists(alt_input):
            input_xacro = alt_input
        else:
            raise FileNotFoundError(f"Cannot find Bipedal_robotics_part_v2.xacro in {BASE_DIR} or {os.path.join(BASE_DIR, 'urdf')}")

    output_urdf = os.path.join(BASE_DIR, "Bipedal_robotics_part_v2.urdf")

    print(f"Reading Xacro: {input_xacro}")
    print(f"Using Package Path: {PACKAGE_FOLDER}")

    # Process xacro into URDF XML DOM
    doc = xacro.process_file(input_xacro)
    xml_content = doc.toprettyxml(indent="  ")

    # Write output URDF
    with open(output_urdf, "w", encoding="utf-8") as f:
        f.write(xml_content)

    # Also save to urdf/ subfolder if it exists
    urdf_subfolder = os.path.join(BASE_DIR, "urdf")
    if os.path.isdir(urdf_subfolder):
        subfolder_urdf = os.path.join(urdf_subfolder, "Bipedal_robotics_part_v2.urdf")
        with open(subfolder_urdf, "w", encoding="utf-8") as f:
            f.write(xml_content)

    print(f"Successfully converted and generated:\n -> {output_urdf}")
    return output_urdf

if __name__ == "__main__":
    convert_xacro_to_urdf()
