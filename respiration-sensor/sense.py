#!/usr/bin/python

"""
sense.py
"""

import sys
from scientisst import *
from scientisst import __version__
from threading import Timer
from threading import Event
from sense_src.custom_script import get_custom_script, CustomScript
from sense_src.file_writer import *


from serial.tools import list_ports

# Create Exception for serial port unavailable (explained at the end of the section)
class SerialPortUnavailable:
    def __init__(self):
        print("Chosen port is not available. Choose one of the following ports:")
        for port in list_ports.comports():
            print(f"    * {port.name}")


def run_scheduled_task(duration, stop_event):
    def stop(stop_event):
        stop_event.set()

    timer = Timer(duration, stop, [stop_event])
    timer.start()
    return timer


class ScientisstArgs:
    def __init__(
        self,
        address,
        channels="1, 2, 3, 4, 5, 6",
        fs=10,
        mode=COM_MODE_BT,
        version=False,
        duration=60,
        log=False,
        output=None,
        convert=True,
        stream=False,
        script=False,
        verbose=True,
    ):
        self.version = version
        self.address = address
        self.mode = mode
        self.duration = duration
        self.channels = channels
        self.fs = fs
        self.log = log
        self.output = output
        self.convert = convert
        self.stream = stream
        self.output = output
        self.script = script
        self.verbose = verbose


def main(address, fs, channels, file_path):

    args = ScientisstArgs(address=address, fs=fs, channels=channels, output=file_path)

    if args.version:
        sys.stdout.write("sense.py version {}\n".format(__version__))

    if args.address:
        address = args.address
    # else:
    #     if args.mode == COM_MODE_BT:
    #         address = DevicePicker().select_device()
    #         if not address:
    #             arg_parser.error("No paired device found")
    #     else:
    #         arg_parser.error("No address provided")

    args.channels = sorted(map(int, args.channels.split(",")))
    try:
        scientisst = ScientISST(address, com_mode=args.mode, log=args.log)
    except serial.SerialException:
        SerialPortUnavailable()

    try:
        if args.output:
            firmware_version = scientisst.version_and_adc_chars(print=False)
            file_writer = FileWriter(
                args.output,
                address,
                args.fs,
                args.channels,
                args.convert,
                __version__,
                firmware_version,
            )
        if args.stream:
            from sense_src.stream_lsl import StreamLSL

            lsl = StreamLSL(
                args.channels,
                args.fs,
                address,
            )
        if args.script:
            script = get_custom_script(args.script)

        stop_event = Event()

        scientisst.start(args.fs, args.channels)
        sys.stdout.write("Start acquisition\n")

        if args.output:
            file_writer.start()
        if args.stream:
            lsl.start()
        if args.script:
            script.start()

        timer = None
        if args.duration > 0:
            timer = run_scheduled_task(args.duration, stop_event)
        try:
            if args.verbose:
                header = "\t".join(get_header(args.channels, args.convert)) + "\n"
                sys.stdout.write(header)
            while not stop_event.is_set():
                frames = scientisst.read(convert=args.convert)
                if args.output:
                    file_writer.put(frames)
                if args.stream:
                    lsl.put(frames)
                if args.script:
                    script.put(frames)
                if args.verbose:
                    sys.stdout.write("{}\n".format(frames[0]))
        except KeyboardInterrupt:
            if args.duration and timer:
                timer.cancel()
            pass

        scientisst.stop()
        # let the acquisition stop before stoping other threads
        time.sleep(0.25)

        sys.stdout.write("Stop acquisition\n")
        if args.output:
            file_writer.stop()
        if args.stream:
            lsl.stop()
        if args.script:
            script.stop()

    finally:
        scientisst.disconnect()


if __name__ == "__main__":
    main()
