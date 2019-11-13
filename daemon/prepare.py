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
        simulatorPath = '../simulators/' + self.ai['name'] + '.py'
        cflags = ['python3', simulatorPath, source]
        child = subprocess32.Popen(cflags, stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
        try:
            self.compile_timeout = False
            self.compile_stdout, self.compile_stderr = child.communicate(timeout=10)
        except subprocess32.TimeoutExpired:
            self.compile_timeout = True
            self.compile_stdout = self.compile_stderr = "Timeout"
            with open(target, 'w', newline='\n') as f:
                f.write(self.compile_stdout)
            return False

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
            if not self.compile_timeout:
                result['error'] = 'Simulation Failed. STDERR:\n' + self.compile_stderr
            else:
                result['status'] = 'timeout'
                result['error'] = 'Simulation Timeout\n'
        else:
            result['status'] = 'success'
            result['abspath'] = self.abspath
            result['info'] = self.compile_stdout + '\n' + self.compile_stderr
        self._clean()
        return result
