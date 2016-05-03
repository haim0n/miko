# Miko

By providing a library name, `Miko` would output which OpenStack projects are using it.

### Installation

```
pip install pygithub
chmod +x miko.py
```

## Usage

To check if any openstack project is using 'mario' library

```
python miko/main.py --library mario
```

To see additional information while running `miko` use the `--debug` flag

```
python miko/main.py --library mario --debug
```

To use your personal user:

```
python miko/main.py --library beautifulsoup4 --user <my_github_username>
```
