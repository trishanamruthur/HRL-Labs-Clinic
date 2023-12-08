# Gitlab Documentation

HRL presumably already has Gitlab set up how they want it. This documentation is here so HRL knows how the clinic team set it up, in case that becomes relevant for troubleshooting or figuring out why something behaves differently on HRL's network.

We installed Gitlab Omnibus on a computer running Ubuntu 22.04 following [these instructions](https://about.gitlab.com/install/#ubuntu). We did not use the Gitlab Ultimate, either as a trial or in full. 

```{admonition} A Clinic Bug
:class: note, dropdown
We ended up putting JupyterHub at port 8080, and this broke Gitlab. It turns out that Gitlab has a process that listens there normally. Go to ```/etc/gitlab/gitlab.rb``` uncomment the ```puma['port'] = 8080``` and change it to e.g. 8081.
```

Add ssh key for computer with [Jupyterhub](Jupyterhub Setup).