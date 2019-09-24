# -*- coding: utf-8 -*-
import subprocess32
import tempfile
import shutil
import glob
from os import path

import const

class Prepare:
    def _compile(self):
        print('      Compiling...')

        # Prepare
        self.tmpdir = tempfile.mkdtemp()
        source = path.join(self.tmpdir, 'source.txt')
        with open(source, 'w', newline='\n') as f:
            f.write(self.ai['sourceCode'])

        # Compile
        target = path.join(self.tmpdir, 'client')
        cflags = ['python3', '../simulators/TuringMachine.py', source]
        child = subprocess32.Popen(cflags, stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
        self.compile_stdout, self.compile_stderr = child.communicate()
        self.compile_stdout = self.compile_stdout.decode('utf-8')
        self.compile_stderr = self.compile_stderr.decode('utf-8')
        with open(target, 'w', newline='\n') as f:
            f.write(self.compile_stdout)

        exitcode = child.returncode
        if exitcode != 0:
            return False

        # Move client to the specific directory
        ai_name = 'ai_' + str(self.ai['_id'])
        self.abspath = path.join(const.AI_SAVE_DIRECTORY, ai_name)
        shutil.move(target, self.abspath)
        return True

    def _clean(self):
        shutil.rmtree(self.tmpdir)

    def __init__(self, ai):
        self.ai = ai

    def Run(self):
        result = { 'status': 'failure' }
        if not self._compile():
            result['error'] = 'Compile Failed. STDERR:\n' + self.compile_stderr
        else:
            result['status'] = 'success'
            result['abspath'] = self.abspath
            result['info'] = self.compile_stdout + '\n' + self.compile_stderr
        self._clean()
        return result
