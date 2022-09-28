
import subprocess
import psutil
import time
import os
import pandas as pd
import netifaces as ni



def Main():


    inter = ni.interfaces()

    interfaces =[]

    for i in inter:
        interfaces.append(ni.ifaddresses(i)[ni.AF_INET][0])

    labels = []

    UPDATE_DELAY = 1  # in seconds

    def get_size(bytes):
        """
        Returns size of bytes in a nice format
        """
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024

    # get the network I/O stats from psutil on each network interface
    # by setting `pernic` to `True`
    io = psutil.net_io_counters(pernic=True)
    print()

    per_cpu = psutil.cpu_percent(percpu=True)
    # For individual core usage with blocking, psutil.cpu_percent(interval=1, percpu=True)
    Data_Cores = []
    Cores = []
    for idx, usage in enumerate(per_cpu):
        print(f"CORE_{idx + 1}: {usage}%")

        Data_Cores.append(f"{usage}%")
        Cores.append(f"Core_{idx}")

    mem_usage = psutil.virtual_memory()

    RAM = [f"{mem_usage.percent}%", f"{mem_usage.total / (1024 ** 3):.2f}G", f"{mem_usage.used / (1024 ** 3):.2f}G"]

    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the network I/O stats again per interface
    io_2 = psutil.net_io_counters(pernic=True)
    # initialize the data to gather (a list of dicts)
    data = []

    for iface, iface_io in io.items():
        # new - old stats gets us the speed
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[
            iface].bytes_recv - iface_io.bytes_recv

        data.append({

            "iface": iface,
            "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
        })
    # update the I/O stats for the next iteration
    io = io_2
    # construct a Pandas DataFrame to print stats in a cool tabular style

    df = pd.DataFrame(data)

    RAM_table = pd.DataFrame(
        data=RAM,

        columns=["Usage - RAM"],

        index=["Free", "Total", "Used"]
    )
    # RAM_table.rename(index={"0" : "Usage"}, inplace=True)
    # RAM_table = RAM_table.T

    PER_CPU = pd.DataFrame(
        data=Data_Cores,

        columns=["Usage of every core"],

        index=Cores
    )

    # sort values per column, feel free to change the column
    df.sort_values("Download", inplace=True, ascending=False)
    # clear the screen based on your OS

    obj_Disk = psutil.disk_usage('/')

    Hard_Drive_Data = [
        f"{obj_Disk.total / (1024.0 ** 3):.2f} GB",

        f"{obj_Disk.used / (1024.0 ** 3):.2f}GB",

        f"{obj_Disk.free / (1024.0 ** 3):.2f}GB",

        f"{obj_Disk.percent}%"]

    Hard_Drive_Table = pd.DataFrame(

        data=Hard_Drive_Data,

        columns=["Usage - Hard drive"],

        index=["Total", "Used", "Free", "Usage(%)"]

    )
    path = os.path.abspath("Scorpio\system_data_readings.txt")
    with open(f"{path}", "w") as file:

        # subprocess.call('ipconfig /all', stdout=file)

        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")

        file.write(RAM_table.to_string())

        file.write("\n")
        file.write("\n")

        file.write(Hard_Drive_Table.to_string())

        file.write("\n")
        file.write("\n")

        file.write(PER_CPU.to_string())

        file.write("\n")
        file.write("\n")

        file.write(df.to_string())

        file.write("\n")
        file.write("\n")

        for i in range(len(interfaces)):
            file.write(inter[i])
            file.write("\n")
            for key, value in interfaces[i].items():
                file.write(f"{key}: {value}")
                file.write("\n")


