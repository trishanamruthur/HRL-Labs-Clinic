import subprocess, os, glob
from argparse import ArgumentParser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class BuildBookEventHandler(FileSystemEventHandler):
    """builds book when it detects the source files have changed."""
    # which file events will trigger a build
    TRIGGERS = ['created', 'deleted', 'modified']

    def __init__(self, src_dir, dest_dir):
        super().__init__()
        # last time a watched file has been modified
        self.last_modify = 0
        # directory of the src files---use absolute path
        self.src_dir = os.path.abspath(src_dir)
        # directory where src is copied and built
        self.dest_dir = os.path.abspath(dest_dir)
        self.buildnum = 0

    def on_any_event(self, event):
        """Build book when an event occurs. Method inherited from super."""
        if event.event_type not in self.TRIGGERS:
            return
        # directories are modified whenever their contents are;
        # avoid those duplicate events.
        # adding/removing empty directories also doesn't matter.
        if event.is_directory:
            return
        # avoid triggering when hidden files are modified,
        # like auto-backups during editing.
        if (event.src_path.split('/')[-1][0] == '.'):
            return
        # editing files creates two events in quick succession. avoid that
        # it would be nice to also prevent simultaneous file deletions from
        # triggering multiple builds, but I'm not sure how to check when
        # the event happened if the file no longer exists.
        if event.event_type == 'modified':
            new_time = os.stat(event.src_path).st_mtime
            if self.last_modify and new_time - self.last_modify < 1:
                return
            self.last_modify = new_time
        if not os.path.isdir(self.dest_dir):
            print("Creating _built directory")
            subprocess.run(["mkdir", self.dest_dir])
        print("Copying files to:", self.dest_dir)

        # get a list of all contents of src_dir. subprocess doesn't glob
        # unless you set shell=True, which is sketchy for multiple reasons
        cp_files = glob.glob(self.src_dir + '/*')
        cp_args = ["cp", "-r"] + cp_files + [self.src_dir, self.dest_dir]
        subprocess.run(cp_args)

        print("Building book")
        subprocess.run(["jupyter-book", "build", self.dest_dir])
        # useful if you want to check terminal to see if book just built
        self.buildnum += 1
        print("Done (this was build " + str(self.buildnum) + ")")

if __name__ == "__main__":
    parser = ArgumentParser(description=
                            'Monitor directory and build Jupyter Book')
    parser.add_argument('src_dir', nargs=1, type=str, 
                        help='path to folder containing all src files')
    args = parser.parse_args()
    src_dir = args.src_dir[0].rstrip('/')
    # copy and build files in folder called '<src_dir>_built'
    event_handler = BuildBookEventHandler(src_dir, src_dir + '_built')
    observer = Observer()
    observer.schedule(event_handler, src_dir, recursive=True)
    observer.start()
    try:
        # continuously check folder for changes. (terminate with ^C or such)
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()