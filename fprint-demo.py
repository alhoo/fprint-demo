import gi

gi.require_version("FPrint", "2.0")
from gi.repository import FPrint, GLib

ctx = FPrint.Context()
devices = ctx.get_devices()
if len(devices) > 0:

    mainloop = GLib.MainLoop()

    def closed(dev, res):
        dev.close_finish(res)
        mainloop.quit()

    def captured(dev, res, *args, **kwargs):
        try:
            image = dev.capture_finish(res)
            print("Captured. Saving to capture.pgm")
            with open("capture.pgm", "wb") as f:
                f.write(
                    (
                        "P5 {} {} 255\n".format(image.get_width(), image.get_height())
                    ).encode()
                )
                f.write(image.get_data())
            try:
                from matplotlib import pyplot as plt
                from matplotlib import image as mpimg

                plt.imshow(mpimg.imread("capture.pgm"))
                plt.show()
            except:
                pass
        except gi.repository.GLib.GError as err:
            print(err)
            dev.capture(True, None, captured)
            pass
        else:
            dev.close(callback=closed)

    def capture(dev, *args, **kwargs):
        print("Waiting for scan")
        dev.capture(True, None, captured)

    def on_device_opened(dev, task, *args, **kwargs):
        error = None
        res = dev.open_finish(task)
        if res == None:
            capture(dev)
        else:
            print("Error")

    devices[0].open(callback=on_device_opened)

    mainloop.run()
