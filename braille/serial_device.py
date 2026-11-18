"""Optional serial output for compatible local Braille devices.

This sends UTF-8 Braille Unicode. Many Braille displays/embossers require a
manufacturer-specific protocol, so this generic transport is only a prototype.
"""

from __future__ import annotations


def list_serial_ports() -> list[str]:
    """Return locally attached serial port names, or an empty list if unavailable."""
    try:
        from serial.tools import list_ports
    except ImportError:
        return []

    return sorted(port.device for port in list_ports.comports())


def send_braille_text(
    braille_text: str,
    port: str,
    baudrate: int = 9600,
    timeout: float = 2.0,
) -> int:
    """Send UTF-8 Braille Unicode to a local serial port.

    Returns the number of bytes written. The caller must ensure that the
    connected device accepts UTF-8 Braille Unicode over a serial connection.
    """
    if not isinstance(braille_text, str) or not braille_text:
        raise ValueError("Braille output is empty")
    if not isinstance(port, str) or not port.strip():
        raise ValueError("Select a serial port")
    if baudrate <= 0:
        raise ValueError("Baud rate must be a positive integer")

    try:
        import serial
    except ImportError as exc:
        raise RuntimeError(
            "pyserial is not installed. Install project dependencies first."
        ) from exc

    payload = braille_text.encode("utf-8")
    try:
        with serial.Serial(port=port, baudrate=baudrate, timeout=timeout) as device:
            return device.write(payload)
    except serial.SerialException as exc:
        raise RuntimeError(f"Could not write to {port}: {exc}") from exc
