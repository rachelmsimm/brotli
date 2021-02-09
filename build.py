# Controls running cmake, building, and copying files to the dist folder for the various
# platforms.
import os
import shutil
import sys
import subprocess

# build the brotli exe using cmake
if not os.path.exists('cmake'):
    os.mkdir('cmake')

os.chdir('cmake')

if sys.platform == 'win32':
    os.system('cmake -G "NMake Makefiles" ..')
    os.system('nmake')
else:
    os.system('cmake -G "Unix Makefiles" ..')
    os.system('make')

os.chdir('..')

# Copy the build to the dist folder
if not os.path.exists('dist'):
    os.mkdir('dist')

if sys.platform == 'win32':
    if not os.path.exists('dist/win_x86_64'):
        os.mkdir('dist/win_x86_64')
    shutil.copy2('cmake/brotli.exe', 'dist/win_x86_64/brotli.exe')
elif sys.platform == 'darwin':
    if not os.path.exists('dist/macos_x86_64'):
        os.mkdir('dist/macos_x86_64')
    shutil.copy2('cmake/brotli', 'dist/macos_x86_64/brotli')
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
