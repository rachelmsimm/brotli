# Controls running cmake, building, and copying files to the dist folder for the various
# platforms.
import os
import shutil
import sys
import subprocess
import json

WINDOWS = False
if os.name == 'nt' or (os.getenv('SYSTEMROOT') is not None and 'windows' in os.getenv('SYSTEMROOT').lower()) or (os.getenv('COMSPEC') is not None and 'windows' in os.getenv('COMSPEC').lower()):
    WINDOWS = True

def vswhere():
    try:
        program_files = os.environ['ProgramFiles(x86)'] if 'ProgramFiles(x86)' in os.environ else os.environ['ProgramFiles']
        vswhere_path = os.path.join(program_files, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
        args = [vswhere_path, '-latest', '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64', '-property', 'installationPath', '-format', 'json']
        output = json.loads(subprocess.check_output(args))
        return str(output[0]['installationPath'])
    except Exception as err:
        return ''

def generate_build_script(platform):
    vs_path = vswhere()
    vcvarsall = os.path.join(vs_path, 'VC\\Auxiliary\\Build\\vcvarsall.bat')
    fp = open('build.bat', 'wt')
    fp.write('call "%s" %s\n' % (vcvarsall, platform))
    fp.write('cmake -G "NMake Makefiles" ..\n')
    fp.write('nmake')
    fp.close()

# build the brotli exe using cmake
if not os.path.exists('cmake'):
    os.mkdir('cmake')

os.chdir('cmake')

if WINDOWS:
    generate_build_script('x86_amd64')
    os.system('build.bat')
else:
    os.system('cmake -G "Unix Makefiles" ..')
    os.system('make')

os.chdir('..')

# Copy the build to the dist folder
if not os.path.exists('dist'):
    os.mkdir('dist')

if WINDOWS:
    if not os.path.exists('dist/win_x86_64'):
        os.mkdir('dist/win_x86_64')
    shutil.copy2('cmake/brotli.exe', 'dist/win_x86_64/brotli.exe')
elif sys.platform == 'darwin':
    if not os.path.exists('dist/macos'):
        os.mkdir('dist/macos')
    shutil.copy2('cmake/brotli', 'dist/macos/brotli')
else:
    if not os.path.exists('dist/linux_x86_64'):
        os.mkdir('dist/linux_x86_64')
    shutil.copy2('cmake/brotli', 'dist/linux_x86_64/brotli')


# Create the commits.txt file
commits = open('dist/commits.txt', 'w')
subprocess.run('git config --get remote.origin.url', shell=True, stdout=commits)
subprocess.run('git rev-parse HEAD', shell=True, stdout=commits)
commits.close()

# Copy license file
shutil.copy2('LICENSE', 'dist/LICENSE.txt')
