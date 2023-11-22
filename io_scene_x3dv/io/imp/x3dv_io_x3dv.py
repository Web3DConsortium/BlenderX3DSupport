# SPDX-License-Identifier: Apache-2.0
# Copyright 2018-2021 The x3dv-Blender-IO authors.

from ...io.com.x3dv_io_path import uri_to_path
from os.path import dirname, join, isfile

import logging
import base64

# Raise this error to have the importer report an error message.
class ImportError(RuntimeError):
    pass


class x3dvImporter():
    """x3dv Importer class."""

    def __init__(self, filename, import_settings):
        """initialization."""
        self.filename = filename
        self.import_settings = import_settings
        self.buffers = {}
        self.accessor_cache = {}
        self.decode_accessor_cache = {}

        if 'loglevel' not in self.import_settings.keys():
            self.import_settings['loglevel'] = logging.ERROR

        log = Log(import_settings['loglevel'])
        self.log = log.logger
        self.log_handler = log.hdlr


    @staticmethod
    def load_json(content):
        def bad_constant(val):
            raise ImportError('Bad x3dv: json contained %s' % val)
        try:
            text = str(content, encoding='utf-8')
            return json.loads(text, parse_constant=bad_constant)
        except ValueError as e:
            raise ImportError('Bad x3dv: json error: %s' % e.args[0])

    def checks(self):
        """Some checks."""
        if self.data.extensions_required is not None:
            for extension in self.data.extensions_required:
                if extension not in self.data.extensions_used:
                    raise ImportError("Extension required must be in Extension Used too")
                if extension not in self.extensions_managed:
                    raise ImportError("Extension %s is not available on this addon version" % extension)

        if self.data.extensions_used is not None:
            for extension in self.data.extensions_used:
                if extension not in self.extensions_managed:
                    # Non blocking error #TODO log
                    pass

    def load_x3d(self, content):
        """Load x3d."""
        return #x3d scene

    def load_x3dv(self, content):
        """Load x3dv."""
        return #x3d scene

    def load_html(self, content):
        """Load html."""
        return #x3d scene

    def read(self):
        """Read file."""
        if not isfile(self.filename):
            raise ImportError("Please select a file")

        with open(self.filename, 'rb') as f:
            content = memoryview(f.read())

        if content[:4] == b'x3dv':
            x3dv, = self.load_glb(content)
        else:
            x3dv = x3dvImporter.load_json(content)
            

        x3dvImporter.check_version(x3dv)

        try:
            self.data = x3dv_from_dict(x3dv)
        except AssertionError:
            import traceback
            traceback.print_exc()
            raise ImportError("Couldn't parse x3dv. Check that the file is valid")


    def load_uri(self, uri):
        """Loads a URI."""
        sep = ';base64,'
        if uri.startswith('data:'):
            idx = uri.find(sep)
            if idx != -1:
                data = uri[idx + len(sep):]
                return memoryview(base64.b64decode(data))

        path = join(dirname(self.filename), uri_to_path(uri))
        try:
            with open(path, 'rb') as f_:
                return memoryview(f_.read())
        except Exception:
            self.log.error("Couldn't read file: " + path)
            return None
