@dataclass
class ModbusConnection:
    """Class defining properties for Modbus connection.

    Attributes:
        port (str): Modbus communication port.
        baud_rate (int): Communication baud rate.
        data_bits (int): Data bits count. Defaults to 8.
        parity (str): Parity setting ("N" for none, "E" for even, "O" for odd). Defaults to "N".
        stop_bits (int): Stop bits count. Defaults to 1.
        timeout (int): Communication timeout (in seconds). Defaults to 10.
    """

    port: str
    baud_rate: int
    data_bits: int = 8
    parity: str = "N"
    stop_bits: int = 1
    timeout: int = 10

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusConnection":
        """Construct ModbusConnection from JSON input.

        Args:
            json_data (Dict[str, Any]): JSON with connection details.

        Returns:
            ModbusConnection: An instance of ModbusConnection.

        Raises:
            ValueError: If fields are missing or invalid in the JSON input.
        """
        port = json_data.get("port")
        baud_rate = json_data.get("baudRate")
        data_bits = json_data.get("byteSize", 8)

        parity_to_internal = {"none": "N", "even": "E", "odd": "O"}
        parity = parity_to_internal.get(json_data.get("parity", "none"), "N")

        stop_bits = json_data.get("stopBits", 1)
        timeout = json_data.get("timeout", 10)

        if not port or not isinstance(port, str):
            raise ValueError("Connection configuration error: 'port' field is required and must be a non-empty string")

        if not isinstance(baud_rate, int) or baud_rate <= 0:
            raise ValueError("Connection configuration error: 'baudRate' field must be a positive integer")

        if data_bits not in [7, 8]:
            raise ValueError("Connection configuration error: 'byteSize' must be either 7 or 8")

        if parity not in parity_to_internal.values():
            raise ValueError("Connection configuration error: 'parity' must be 'none', 'even', or 'odd'")

        if stop_bits not in [1, 1.5, 2]:
            raise ValueError("Connection configuration error: 'stopBits' must be 1, 1.5, or 2")

        if timeout <= 0:
            raise ValueError("Connection configuration error: 'timeout' must be a positive number")

        return cls(port, baud_rate, data_bits, parity, stop_bits, timeout)


@dataclass
class ModbusSignal:
    """Class representing a standalone Modbus signal.

    Attributes:
        address (int): Address of the Modbus signal.
        name (str): Name of the Modbus signal.
        data_type (str): Data type of the Modbus signal.
        count (int): Data count for the Modbus signal. Defaults to 1.
        k (int): Value of k for the Modbus signal. Defaults to 1.
    """

    address: int
    name: str
    data_type: str
    count: int = 1
    k: int = 1

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusSignal":
        """Build ModbusSignal instance from JSON data.

        Args:
            json_data (Dict[str, Any]): JSON with signal details.

        Returns:
            ModbusSignal: A new instance.

        Raises:
            ValueError: If necessary fields are missing or invalid in the JSON.
        """
        address = json_data.get("address")
        name = json_data.get("name")
        data_type = json_data.get("type")
        count = json_data.get("count", 1)
        k = json_data.get("k", 1)

        if address is None:
            raise ValueError("Signal configuration error: 'address' field is required for standalone signals")

        if name is None:
            raise ValueError("Signal configuration error: 'name' field is required for standalone signals")

        if data_type is None:
            raise ValueError("Signal configuration error: 'type' field is required for standalone signals")

        if count is None or not isinstance(count, int) or count <= 0:
            raise ValueError("Signal configuration error: 'count' must be a positive integer")

        if k is None or not isinstance(k, int) or k <= 0:
            raise ValueError("Signal configuration error: 'k' must be a positive integer")

        # Handle hexadecimal address format
        if isinstance(address, str):
            if not address.startswith("0x"):
                raise ValueError(f"Signal configuration error: Invalid address format '{address}'. Hexadecimal addresses must start with '0x'")

            try:
                address = int(address, 16)
            except ValueError:
                raise ValueError(f"Signal configuration error: Invalid hexadecimal address '{address}'")

        if not isinstance(address, int) or address < 0:
            raise ValueError("Signal configuration error: 'address' must be a non-negative integer or valid hexadecimal string")

        return cls(address, name, data_type, count, k)


@dataclass
class ModbusGroupSignal:
    """Class representing a Modbus signal within a group.

    Attributes:
        address (Optional[int]): Address of the Modbus signal (can be None for group signals).
        name (Optional[str]): Name of the Modbus signal (can be None if skip is specified).
        data_type (Optional[str]): Data type of the Modbus signal (can be None for group signals).
        count (int): Data count for the Modbus signal. Defaults to 1.
        k (int): Value of k for the Modbus signal. Defaults to 1.
        skip (Optional[int]): Number of positions to skip in the group.
    """

    address: Optional[int] = None
    name: Optional[str] = None
    data_type: Optional[str] = None
    count: int = 1
    k: int = 1
    skip: Optional[int] = None

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusGroupSignal":
        """Build ModbusGroupSignal instance from JSON data.

        Args:
            json_data (Dict[str, Any]): JSON with signal details.

        Returns:
            ModbusGroupSignal: A new instance.

        Raises:
            ValueError: If necessary fields are missing or invalid in the JSON.
        """
        address = json_data.get("address")
        name = json_data.get("name")
        data_type = json_data.get("type")
        count = json_data.get("count", 1)
        k = json_data.get("k", 1)
        skip = json_data.get("skip")

        # For group signals, name is required only if skip is not specified
        if skip is None and name is None:
            raise ValueError("Group signal configuration error: 'name' field is required when 'skip' is not specified")

        if count is None or not isinstance(count, int) or count <= 0:
            raise ValueError("Group signal configuration error: 'count' must be a positive integer")

        if k is None or not isinstance(k, int) or k <= 0:
            raise ValueError("Group signal configuration error: 'k' must be a positive integer")

        if skip is not None and (not isinstance(skip, int) or skip <= 0):
            raise ValueError("Group signal configuration error: 'skip' must be a positive integer when specified")

        # Handle hexadecimal address format if provided
        if isinstance(address, str):
            if not address.startswith("0x"):
                raise ValueError(f"Group signal configuration error: Invalid address format '{address}'. Hexadecimal addresses must start with '0x'")

            try:
                address = int(address, 16)
            except ValueError:
                raise ValueError(f"Group signal configuration error: Invalid hexadecimal address '{address}'")

        if address is not None and (not isinstance(address, int) or address < 0):
            raise ValueError("Group signal configuration error: 'address' must be a non-negative integer or valid hexadecimal string when specified")

        return cls(address, name, data_type, count, k, skip)


@dataclass
class ModbusGroup:
    """Class representing a Modbus group containing multiple signals.

    Attributes:
        name (str): Name of the group.
        start_address (int): Starting address for the group.
        signals (List[ModbusGroupSignal]): List of signals in the group.
        data_type (Optional[str]): Data type of the group (currently only 'bit' is supported).
        nbytes (Optional[int]): Number of bytes for bit-type groups.
    """

    name: str
    start_address: int
    signals: List[ModbusGroupSignal]
    data_type: Optional[str] = None
    nbytes: Optional[int] = None

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusGroup":
        """Construct ModbusGroup instance from JSON data.

        Args:
            json_data (Dict[str, Any]): JSON with group details.

        Returns:
            ModbusGroup: A new ModbusGroup instance.

        Raises:
            ValueError: If fields are missing or invalid in the JSON.
        """

        name = json_data.get("name")
        start_address = json_data.get("startAddress")
        signals_data: Optional[List[Dict[str, Any]]] = json_data.get("signals")
        data_type = json_data.get("type")
        nbytes = json_data.get("bytes")

        if name is None:
            raise ValueError("Group configuration error: 'name' field is required")

        if start_address is None:
            raise ValueError(f"Group configuration error: 'startAddress' field is required for group '{name}'")

        if data_type is not None and data_type != "bit":
            raise ValueError(f"Group configuration error: Only 'bit' type is supported for groups, got '{data_type}' in group '{name}'")

        if data_type == "bit" and nbytes is None:
            raise ValueError(f"Group configuration error: 'bytes' field is required when type is 'bit' in group '{name}'")

        if not signals_data:
            raise ValueError(f"Group configuration error: At least one signal must be defined in group '{name}'")

        # Handle hexadecimal start address format
        if isinstance(start_address, str):
            if not start_address.startswith("0x"):
                raise ValueError(f"Group configuration error: Invalid startAddress format '{start_address}' in group '{name}'. Hexadecimal addresses must start with '0x'")

            try:
                start_address = int(start_address, 16)
            except ValueError:
                raise ValueError(f"Group configuration error: Invalid hexadecimal startAddress '{start_address}' in group '{name}'")

        if not isinstance(start_address, int) or start_address < 0:
            raise ValueError(f"Group configuration error: 'startAddress' must be a non-negative integer or valid hexadecimal string in group '{name}'")

        if nbytes is not None and (not isinstance(nbytes, int) or nbytes <= 0):
            raise ValueError(f"Group configuration error: 'bytes' must be a positive integer in group '{name}'")

        signals = [ModbusGroupSignal.from_json(signal) for signal in signals_data]

        return cls(name, start_address, signals, data_type, nbytes)


@dataclass
class ModbusDevice:
    """Class defining a Modbus device.

    Attributes:
        slave_id (int): Slave ID of the device.
        name (str): Name of the device.
        poll_period (int): Poll period in seconds.
        signals (List[ModbusSignal]): List of standalone signals for the device.
        groups (List[ModbusGroup]): List of signal groups for the device.
        byte_order (Endian): Values could be LITTLE, BIG or AUTO.
        word_order (Endian): Values could be LITTLE, BIG or AUTO.
    """

    slave_id: int
    name: str
    poll_period: int
    signals: List[ModbusSignal]
    groups: List[ModbusGroup]
    byte_order: Endian = Endian.LITTLE
    word_order: Endian = Endian.BIG

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ModbusDevice":
        """Create ModbusDevice from JSON input.

        Args:
            json_data (Dict[str, Any]): JSON containing device details.

        Returns:
            ModbusDevice: A new ModbusDevice instance.

        Raises:
            ValueError: If required data is missing or invalid in JSON.
        """
        ORDER_MAPPING = {"lt": Endian.LITTLE, "be": Endian.BIG, "auto": Endian.AUTO}

        slave_id = json_data.get("slaveId")
        name = json_data.get("name")
        poll_period = json_data.get("pollPeriod", 60)
        byte_order_str = json_data.get("byteOrder", "lt")
        word_order_str = json_data.get("wordOrder", "be")
        signals_data: Optional[List[Dict[str, Any]]] = json_data.get("signals", [])
        groups_data: Optional[List[Dict[str, Any]]] = json_data.get("groups", [])

        if slave_id is None:
            raise ValueError("Device configuration error: 'slaveId' field is required")

        if name is None:
            raise ValueError("Device configuration error: 'name' field is required")

        if not isinstance(slave_id, int) or slave_id < 0:
            raise ValueError(f"Device configuration error: 'slaveId' must be a non-negative integer in device '{name}'")

        if not isinstance(poll_period, int) or poll_period <= 0:
            raise ValueError(f"Device configuration error: 'pollPeriod' must be a positive integer in device '{name}'")

        byte_order = ORDER_MAPPING.get(byte_order_str)
        if byte_order is None:
            raise ValueError(f"Device configuration error: 'byteOrder' must be 'lt', 'be', or 'auto', got '{byte_order_str}' in device '{name}'")

        word_order = ORDER_MAPPING.get(word_order_str)
        if word_order is None:
            raise ValueError(f"Device configuration error: 'wordOrder' must be 'lt', 'be', or 'auto', got '{word_order_str}' in device '{name}'")

        if not signals_data and not groups_data:
            raise ValueError(f"Device configuration error: At least one signal or group must be defined in device '{name}'")

        signals = [ModbusSignal.from_json(signal) for signal in signals_data] if signals_data else []
        groups = [ModbusGroup.from_json(group) for group in groups_data] if groups_data else []

        return cls(slave_id, name, poll_period, signals, groups, byte_order, word_order)
