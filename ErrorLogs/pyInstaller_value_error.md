# [PyInstaller] Solution for ValueError: cannot load imports from non-existent stub

This error occurs when PyInstaller fails to correctly resolve dependencies for certain modules (often scientific computing libraries). The following steps are likely to resolve the issue.

## 1. Creating Custom Hooks

Create a dedicated custom hook for the problematic module.

1. Create an `extra-hooks` folder in your project root.

2. Create a `hook-problematic_module.py` file inside the `extra-hooks` folder.
   Example: `hook-skimage.metrics.py`

3. Write the following content in the hook file:

```python
# Example of a custom hook
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('problematic_module')
datas = collect_data_files('problematic_module')
```

## 2. Modifying the .spec File

Modify the PyInstaller .spec file as follows:

```python
a = Analysis(
    ['your_script.py'],
    pathex=['path/to/your/script'],
    binaries=[],
    datas=[],
    hiddenimports=['problematic_module', 'problematic_module.*'],  # Add the problematic module and its submodules here
    hookspath=['extra-hooks'],  # Specify the path to custom hooks
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# The rest of the .spec file remains unchanged
```

## 3. Explicit Imports

At the beginning of your main script (`your_script.py`), explicitly import the problematic module:

```python
# Example of imports in the main script
import problematic_module
import problematic_module.submodule
```

## 4. Updating Dependent Libraries

Update related libraries to their latest versions:

```
# Example of library upgrade
pip install --upgrade problematic_library
```

For example, if the error is related to scikit-image:

```
pip install --upgrade scikit-image scipy numpy
```

## 5. Using Virtual Environments

It's recommended to create and work in a virtual environment to manage dependencies in a clean environment:

```
# Example of installing necessary libraries in a virtual environment
python -m venv your_env
your_env\Scripts\activate  # Windows
source your_env/bin/activate  # Mac/Linux
pip install required_libraries
pip install pyinstaller
```

## 6. Re-running PyInstaller

After applying the above changes, recreate the exe file with the following command:

```
pyinstaller --clean your_script.spec
```

## 7. Using Debug Mode

If the problem persists, you can use PyInstaller's debug mode to get more detailed information:

```
pyinstaller --clean --debug all your_script.spec
```

This will provide more detailed error information that may help identify the problem.

## Notes

- Module names or specific paths included in error messages may vary depending on your environment and project. Please replace them with appropriate module names or paths as needed.
- This issue often occurs when using scientific computing libraries (scikit-image, scipy, numpy, etc.).
- In most cases, following these steps in order can solve the problem. However, if it remains unresolved, it's recommended to check the official documentation or community forums of the libraries you're using.

By carefully executing these steps, you're likely to resolve the "ValueError: cannot load imports from non-existent stub" error.

## Examples of Similar Error Messages That Can Be Resolved Using This Method

The following error messages can potentially be resolved by applying the above solutions:

1. `ModuleNotFoundError: No module named 'sklearn'`
   - Occurs when the scikit-learn library is not properly packaged.

2. `ImportError: cannot import name 'imread' from 'scipy.misc'`
   - Occurs when specific functions or submodules of scipy are not found.

3. `AttributeError: module 'numpy' has no attribute 'float'`
   - Occurs when specific attributes or methods of numpy are not found.

4. `ImportError: DLL load failed: The specified module could not be found.`
   - Occurs when necessary DLL files are not found (especially in Windows environments).

5. `OSError: [WinError 126] The specified module could not be found`
   - Similar to the DLL error above, occurs when modules or libraries are not found.

6. `RuntimeError: module compiled against API version 0xb but this version of numpy is 0xa`
   - Occurs due to version mismatches of libraries.

7. `ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject`
   - Occurs due to version mismatches of numpy or its dependent libraries.

8. `ImportError: cannot import name 'PILLOW_VERSION' from 'PIL'`
   - Occurs when there's an issue with the Pillow library version or when it's not properly packaged.

9. `AttributeError: module 'cv2' has no attribute 'imread'`
   - Occurs when specific functions of OpenCV (cv2) are not found.

These errors occur due to dependency issues, library version mismatches, or when PyInstaller fails to properly package specific modules or functions. Applying the above solutions is likely to resolve these issues as well.

---
- Created: 2024-9-3
- Updated: 2024-9-3