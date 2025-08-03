# 📜 module_discovery.py

**File:** `/Users/operator/🌌_COSMIC_ROOT/.beast/consciousness/module_discovery.py`
**Size:** 8027 bytes
**Lines:** 213
**Complexity:** 59
**Last Modified:** 2025-08-03T12:44:09.184533
**Content Hash:** `1ba00e6afca3ed8e`

## 📝 Module Description

🜄 MODULE DISCOVERY SYSTEM 🜄
Auto-discovery and management of evolution modules

## 🔗 Imports

- `os`
- `ast`
- `importlib.util`
- `pathlib.Path`
- `typing.Dict`
- `typing.List`
- `typing.Any`
- `typing.Optional`
- `yaml`

## 🏗️ Classes

### 🧬 ModuleDiscovery

Auto-discovery system for evolution modules

**Location:** Lines 14-186

#### Methods

##### `__init__(self, beast_root)`

**Location:** Lines 19-23

##### `discover_modules(self)`

Discover all available modules in all directories.

**Location:** Lines 25-32

##### `_scan_directory(self, directory)`

Scan a directory for Python modules and extract metadata.

**Location:** Lines 34-49

##### `_extract_module_info(self, file_path)`

Extract metadata from a Python module file.

**Location:** Lines 51-97

##### `_extract_imports(self, tree)`

Extract import statements from AST.

**Location:** Lines 99-111

##### `list_modules(self, category)`

List all discovered modules.

**Location:** Lines 113-141

##### `get_module_summary(self)`

Get a summary of all modules.

**Location:** Lines 143-161

##### `find_module_by_name(self, name)`

Find a specific module by name.

**Location:** Lines 163-173

##### `get_available_evolution_paths(self)`

Get list of available evolution paths for the beast.

**Location:** Lines 175-186

