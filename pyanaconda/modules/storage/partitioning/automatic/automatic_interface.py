#
# DBus interface for the auto partitioning module.
#
# Copyright (C) 2018 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from dasbus.server.interface import dbus_interface
from dasbus.server.property import emits_properties_changed
from dasbus.typing import *  # pylint: disable=wildcard-import
from pyanaconda.modules.common.constants.objects import AUTO_PARTITIONING
from pyanaconda.modules.common.structures.partitioning import PartitioningRequest
from pyanaconda.modules.storage.partitioning.base_interface import PartitioningInterface


@dbus_interface(AUTO_PARTITIONING.interface_name)
class AutoPartitioningInterface(PartitioningInterface):
    """DBus interface for the auto partitioning module."""

    def connect_signals(self):
        """Connect the signals."""
        super().connect_signals()
        self.watch_property("Enabled", self.implementation.enabled_changed)
        self.watch_property("Request", self.implementation.request_changed)

    @property
    def Enabled(self) -> Bool:
        """Is the auto partitioning enabled?"""
        return self.implementation.enabled

    @emits_properties_changed
    def SetEnabled(self, enabled: Bool):
        """Is the auto partitioning enabled?

        :param enabled: True if the autopartitioning is enabled, otherwise False
        """
        self.implementation.set_enabled(enabled)

    @property
    def Request(self) -> Structure:
        """The partitioning request."""
        return PartitioningRequest.to_structure(self.implementation.request)

    @emits_properties_changed
    def SetRequest(self, request: Structure):
        """Set the partitioning request.

        :param request: a request
        """
        self.implementation.set_request(PartitioningRequest.from_structure(request))

    def RequiresPassphrase(self) -> Bool:
        """Is the default passphrase required?

        :return: True or False
        """
        return self.implementation.requires_passphrase()

    @emits_properties_changed
    def SetPassphrase(self, passphrase: Str):
        """Set a default passphrase for all encrypted devices.

        :param passphrase: a string with a passphrase
        """
        self.implementation.set_passphrase(passphrase)

    def RemoveDevice(self, device_name: Str):
        """Remove a device after removing its dependent devices.

        If the device is protected, do nothing. If the device has
        protected children, just remove the unprotected ones.

        :param device_name: a name of the device
        """
        self.implementation.remove_device(device_name)

    def ShrinkDevice(self, device_name: Str, size: UInt64):
        """Shrink the size of the device.

        :param device_name: a name of the device
        :param size: a new size in bytes
        """
        self.implementation.shrink_device(device_name, size)

    def IsDevicePartitioned(self, device_name: Str) -> Bool:
        """Is the specified device partitioned?

        :param device_name: a name of the device
        :return: True or False
        """
        return self.implementation.is_device_partitioned(device_name)

    def GetDevicePartitions(self, device_name: Str) -> List[Str]:
        """Get partitions of the specified device.

        :param device_name: a name of the device
        :return: a list of device names
        """
        return self.implementation.get_device_partitions(device_name)

    def IsDeviceResizable(self, device_name: Str) -> Bool:
        """Is the specified device resizable?

        :param device_name: a name of the device
        :return: True or False
        """
        return self.implementation.is_device_resizable(device_name)

    def GetDeviceSizeLimits(self, device_name: Str) -> Tuple[UInt64, UInt64]:
        """Get size limits of the given device.

        :param device_name: a name of the device
        :return: a tuple of min and max sizes in bytes
        """
        return self.implementation.get_device_size_limits(device_name)