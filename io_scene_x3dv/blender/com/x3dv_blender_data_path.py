# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The x3dv-Blender-IO authors.


def get_target_property_name(data_path: str) -> str:
    """Retrieve target property."""
    return data_path.rsplit('.', 1)[-1]


def get_target_object_path(data_path: str) -> str:
    """Retrieve target object data path without property"""
    path_split = data_path.rsplit('.', 1)
    self_targeting = len(path_split) < 2
    if self_targeting:
        return ""
    return path_split[0]

