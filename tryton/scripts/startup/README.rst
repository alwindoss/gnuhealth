.. SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Creating a Systemd service for the GNU Health server

If you use the standard installation method, you can use the following scripts to automate the startup/stop of the GNU Health instance using systemd services.
GNU Health service unit file

Create the GNU Health Unit file under /usr/lib/systemd/system/gnuhealth.service:

For Ubuntu 18.04 LTS users: /etc/systemd/system/gnuhealth.service:

[Unit]
Description=GNU Health Server
After=network.target

[Service]
Type=simple
User=gnuhealth
WorkingDirectory=/home/gnuhealth
ExecStart=/home/gnuhealth/start_gnuhealth.sh
Restart=on-abort

[Install]
WantedBy=multi-user.target

Starting and Stopping the GNU Health service

You can issue the commands:

systemctl start gnuhealth

or:

systemctl stop gnuhealth

Enable the service to start at boot time

If you want to automatically start the GNU Health server whenever you start the operating system, you can enable the service with the following command:

systemctl enable gnuhealth

