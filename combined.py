import param
from dask.distributed import Client
import posixpath
from visualizer.utils import *
from visualizer.fiveD import grapher
from visualizer.grapher3D import grapher3D as grapher3D
import argparse

# try import RASHG.instruments_RASHG
pn.extension('plotly')
hv.extension('bokeh', 'plotly')
from dask.diagnostics import ProgressBar
import RASHG

pbar = ProgressBar()
pbar.register()


class viewer(param.Parameterized):
    extensions = {'3nc': grapher3D, "5nc": grapher, "5ncu": grapher, "5nce": grapher, "5nca": grapher}
    files = getDir(extensions)
    if posixpath.exists("data/truncated_1.5ncu"):
        default = Path("data/truncated_1.5ncu")
    else:
        default = Path("data/truncated_1.5nc")
    filename = param.ObjectSelector(default=default, objects=files)

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.load()

    def reload_files(self):
        extensions = {'3nc': grapher3D, "5nc": grapher, "5ncu": grapher, "5nce": grapher, "5nca": grapher}
        self.param["filename"].objects = getDir(extensions)

    @param.depends('filename', watch=True)
    def load(self):
        self.reload_files()  # temp solution
        self.grapher = self.extensions[extension(self.filename)](self.filename, self.client)

    @param.depends('filename')
    def widgets(self):
        return pn.Column(self.param, self.grapher.widgets())

    @param.depends('filename')
    def gView(self):
        return self.grapher.view()

    def view(self):
        return pn.Row(self.widgets, self.gView)


class instrumental(param.Parameterized):
    instruments = []
    if RASHG.random_enabled:
        instruments.append("random")
    else:
        print("Random initialization falied, check your environment. This will almost certainly break the program")
    if RASHG.RASHG_enabled:
        instruments.append("RASHG")

    def widgets(self):
        return self.param

    def gView(self):
        pass


# wrapper around viewer class to interface with instrumental class
class combined(param.Parameterized):
    applets = ["viewer", "instrumental"]
    applets = param.ObjectSelector(default="viewer", objects=applets)

    def __init__(self):
        super().__init__()
        self.client = Client()
        client = self.client
        self.load()

    @param.depends('applets', watch=True)
    def load(self):
        if self.applets == "viewer":
            self.applet = viewer(self.client)
        elif self.applets == "instrumental":
            self.applet = instrumental()

    @param.depends('applets')
    def widgets(self):
        return self.applet.widgets()

    @param.depends('applets')
    def gView(self):
        return self.applet.gView()

    def view(self):
        return pn.Row(pn.Column(self.param, self.widgets), self.gView)


# these two functions are basically identical for now
def local():
    view = combined()
    view.view().show()


def server(reload=False):
    view = viewer()
    view.view().show(port=5006, open=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='combined', description='Deploys and runs panel server')
    parser.add_argument('-server', dest='server', help='Runs the panel server for multiple clients',
                        action='store_const', const=True, default=False)
    parser.add_argument('-local', dest='local', help='Runs the panel server for single clients', action='store_const',
                        const=True, default=False)
    args = parser.parse_args()
    if args.server:
        server()
    elif args.local:
        local()
    else:
        print("Defaulting to local server")
        local()
