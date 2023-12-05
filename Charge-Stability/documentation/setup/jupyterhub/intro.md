# Jupyter Hub Setup

Instructions for installing The Littlest Jupyterhub. See [here](https://tljh.jupyter.org/en/latest/) for TLJH's own documentation. TLJH is intended for at most 100 users. If this is not enough for HRL's needs, consider using [Zero to JupyterHub with Kubernetes](https://z2jh.jupyter.org/en/stable/) instead. Note: Zero to Jupyterhub is not officially supported for on-prem Kubernetes clusters. See [here](https://z2jh.jupyter.org/en/stable/kubernetes/other-infrastructure/step-zero-other.html) for more information.

## Installation

TLJH requires a server running Ubuntu 20.04+, with python, curl, and git (probably those are already there). It also may need Jupyter (```(pip|conda) install jupyter```); the installation instructions make no mention of it but the clinic team needed to install it to get TLJH working. Get and run the TLJH installer with

    curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin <admin-user-name>
Replace ```<admin-user-name>``` whatever you want the initial admin user to be called. Don't run the above command from within a conda environment. The installer creates its own environment to run the Hub from.

If exceptions are raised during the installation process, check ```/opt/tljh/installer.log``` for more info. If for some reason you want to remove whatever was installed up to that point to start fresh, do so with

    sudo rm -rf /opt/tljh
    sudo delgroup jupyterhub-users
    sudo delgroup jupyterhub-admins
    sudo rm /etc/sudoers.d/jupyterhub-admins

Probably the first command will be sufficient; all other commands relate to the very last parts of installation. After running the JupyterHub, completely uninstalling it is extremely difficult. So, be certain it's installed where you want it before proceeding.

Check if JupyterHub is running with

    service jupyterhub status
If it isn't, start it with

    sudo service jupyterhub start

## First Steps

Go to the server's IP address. TLJH listens on ports 80 and 443 by default; if you want to change this, run

    sudo tljh-config set http.port <port number>
    sudo tljh-config set https.port <port number>
    sudo tljh-config reload
This is not a very secure thing to do, but the clinic team did it as a low-effort way to run it and the site on the same machine.

The page should have an orange "sign-in" box with fields for username and password. For the username, use whatever ```<admin-user-name>``` you chose during the installation process. Choose a password and type it into the password field; TLJH will remember it for future login attempts. There are no mechanisms for ensuring you typed the password you wanted, so make sure you enter it correctly the first time.

```{admonition} A Clinic Bug
:class: note, dropdown
When installing TLJH the second time, we encountered a bug where the server would time out after 30 seconds with the message "Spawn failed: Server at <IP> didn't respond in 30 seconds." Further [investigation](tljh:troubleshooting) found that TLJH couldn't find jupyter_core. For some reason, jupyter had never been installed in TLJH's environment. We didn't run into the issue the first time, and have no idea why it happened the second time. But, there was little guidance on the interwebs about this issue specifically in relation to TLJH, so here's how we solved it, in case you run into the same issue:

    cd /opt/tljh
Change ownership so that conda can write to the relevant site-packages location. \<username\> is whoever you're logged in as on the Ubuntu server, rather than a TLJH user or the like.

    sudo chown -R <username> user
Install jupyter in the correct environment, and undo everything else.

    conda activate /opt/tljh/user
    conda install jupyter
    conda deactivate
    sudo chown -R root user
```

## Adding New Users

When logged in as an administrator (e.g. the account you logged into above), click File>Hub Control Panel. Click the "Admin" tab at the top left. Click "Add Users." Enter new usernames, one per line. When said user logs in for the first time, whatever they enter in the password field will be remembered later, exactly the process for your administrator account. 

## Installing Packages

To install new packages, open up a terminal from the main page of the Jupyter Hub (while logged in as an administrator). Install packages with pip or conda, but make sure to prepend ```sudo -E``` to any such commands. For example:

    sudo -E conda install -c bokeh bokeh

(tljh:troubleshooting)=
## Troubleshooting

See https://tljh.jupyter.org/en/latest/troubleshooting/logs.html. Yes, the hyphen in the user log command is really there. Bizarre.

## Miscellaneous

TLJH is managed by systemd, and can be started, stopped, etc. with ```systemctl``` or ```service``` commands. ```sudo tljh-config reload``` will restart the Hub without affecting current users. 