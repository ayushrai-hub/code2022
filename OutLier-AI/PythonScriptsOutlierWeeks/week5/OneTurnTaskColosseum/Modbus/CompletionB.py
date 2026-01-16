# config.py  (excerpt – only the parts that changed / were added)
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------- #
# Helper enum and tiny logger stub (unchanged)
# --------------------------------------------------------------------------- #
class Endian(Enum):
    LITTLE = auto()
    BIG = auto()
    AUTO = auto()


class Log:                                 # keep the tiny stub for this snippet
    @staticmethod
    def error(msg: str) -> None:
        print(f"[ERROR] {msg}")


# --------------------------------------------------------------------------- #
# 1.  Stand‑alone Modbus signal
# --------------------------------------------------------------------------- #
@dataclass
class ModbusSignal:
    """A *stand‑alone* Modbus signal (lives directly under a device)."""

    address: int
    name: str
    data_type: str
    count: int = 1
    k: int = 1

    # ---------- factory ----------------------------------------------------- #
    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusSignal":
        """Parse a stand‑alone signal from JSON (address **mandatory**)."""
        address = json_data.get("address")
        name = json_data.get("name")
        data_type = json_data.get("type")
        count = json_data.get("count", 1)
        k = json_data.get("k", 1)

        # ---- validation ---------------------------------------------------- #
        if address is None:
            raise ValueError("'address' can't be undefined for a stand‑alone signal")
        if name is None:
            raise ValueError("'name' can't be undefined for a stand‑alone signal")
        if data_type is None:
            raise ValueError("'type' can't be undefined for a stand‑alone signal")

        # hexadecimal address support
        if isinstance(address, str):
            if not address.startswith("0x"):
                Log.error(f"Invalid address format: {address}")
                raise ValueError(f"Invalid address format: {address}")
            try:
                address = int(address, 16)
            except ValueError:
                Log.error(f"Invalid hexadecimal address: {address}")
                raise ValueError(f"Invalid hexadecimal address: {address}")

        return cls(address, name, data_type, count, k)


# --------------------------------------------------------------------------- #
# 2.  Signal that belongs to a group
# --------------------------------------------------------------------------- #
@dataclass
class ModbusGroupSignal:
    """
    A signal that is **inside** a ModbusGroup.
    - It does *not* carry its own absolute address.
    - It may specify `skip` bytes/bits relative to the previous element.
    """

    name: str
    data_type: Optional[str] = None  # optional when group type == 'bit'
    count: int = 1
    k: int = 1
    skip: Optional[int] = None

    # ---------- factory ----------------------------------------------------- #
    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusGroupSignal":
        name = json_data.get("name")
        data_type = json_data.get("type")
        count = json_data.get("count", 1)
        k = json_data.get("k", 1)
        skip = json_data.get("skip")

        # ---- validation ---------------------------------------------------- #
        if name is None:
            raise ValueError("'name' can't be undefined for a group signal")
        if count is None:
            raise ValueError("'count' can't be undefined for a group signal")
        if k is None:
            raise ValueError("'k' can't be undefined for a group signal")

        return cls(name, data_type, count, k, skip)


# --------------------------------------------------------------------------- #
# 3.  Group of signals
# --------------------------------------------------------------------------- #
@dataclass
class ModbusGroup:
    name: str
    start_address: int
    signals: List[ModbusGroupSignal]
    data_type: Optional[str] = None
    nbytes: Optional[int] = None

    # ---------- factory ----------------------------------------------------- #
    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusGroup":
        name = json_data.get("name")
        start_address = json_data.get("startAddress")
        signals_data: Optional[List[Dict[str, Any]]] = json_data.get("signals")
        data_type = json_data.get("type")
        nbytes = json_data.get("bytes")

        # ---- validation ---------------------------------------------------- #
        if name is None:
            raise ValueError("'name' can't be undefined!")
        if start_address is None:
            raise ValueError("'startAddress' can't be undefined!")
        if data_type is not None and data_type != "bit":
            raise ValueError("The only supported 'type' for the group is 'bit'")
        if data_type == "bit" and nbytes is None:
            raise ValueError("You must set the number of bytes to transform into bits")
        if not signals_data:
            raise ValueError(f"You have to add at least one signal to the group '{name}'")

        # hexadecimal address support
        if isinstance(start_address, str):
            if not start_address.startswith("0x"):
                Log.error(f"Invalid address format: {start_address}")
                raise ValueError(f"Invalid address format: {start_address}")
            try:
                start_address = int(start_address, 16)
            except ValueError:
                Log.error(f"Invalid hexadecimal address: {start_address}")
                raise ValueError(f"Invalid hexadecimal address: {start_address}")

        # parse inner signals with the *group* factory
        signals = [ModbusGroupSignal.from_json(s) for s in signals_data]

        return cls(name, start_address, signals, data_type, nbytes)


# --------------------------------------------------------------------------- #
# 4.  Device (unchanged except for the new class names)
# --------------------------------------------------------------------------- #
@dataclass
class ModbusDevice:
    slave_id: int
    name: str
    poll_period: int
    signals: List[ModbusSignal]
    groups: List[ModbusGroup]
    byte_order: Endian = Endian.LITTLE
    word_order: Endian = Endian.BIG

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusDevice":
        ORDER_MAPPING = {"lt": Endian.LITTLE, "be": Endian.BIG, "auto": Endian.AUTO}

        slave_id = json_data.get("slaveId")
        name = json_data.get("name")
        poll_period = json_data.get("pollPeriod", 60)
        byte_order = ORDER_MAPPING.get(json_data.get("byteOrder", "lt"), Endian.LITTLE)
        word_order = ORDER_MAPPING.get(json_data.get("wordOrder", "be"), Endian.BIG)
        signals_data: Optional[List[Dict[str, Any]]] = json_data.get("signals")
        groups_data: Optional[List[Dict[str, Any]]] = json_data.get("groups")

        # ---- validation ---------------------------------------------------- #
        if slave_id is None:
            raise ValueError("'slaveId' can't be undefined!")
        if name is None:
            raise ValueError("'name' can't be undefined!")
        if poll_period is None:
            raise ValueError("'pollPeriod' can't be undefined!")
        if not isinstance(byte_order, Endian):
            raise ValueError("'byteOrder' is invalid, must be 'lt', 'be', 'auto'")
        if not isinstance(word_order, Endian):
            raise ValueError("'wordOrder' is invalid, must be 'lt', 'be', 'auto'")

        # parse children ----------------------------------------------------- #
        signals = [ModbusSignal.from_json(s) for s in (signals_data or [])]
        groups = [ModbusGroup.from_json(g) for g in (groups_data or [])]

        return cls(
            slave_id=slave_id,
            name=name,
            poll_period=poll_period,
            signals=signals,
            groups=groups,
            byte_order=byte_order,
            word_order=word_order,
        )
