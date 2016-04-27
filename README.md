# Miko
Tells you which OpenStack projects use specific library

### Installation

```
pip install pygithub
chmod +x miko.py
```

## Usage

To check if any openstack project is using 'mario' library

```
./mikoi.py --library mario
```

To see results while it scanning use the `debug` flag

```
./mikoi.py --library mario --debug
```

To use you personal user:

```
./miko.py --library luigi --user <your_github_username>
```
