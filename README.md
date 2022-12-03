# Polly

Polly is a small moking server. It acts as a proxy / caching. It is able to capture live traffic an replaying it afterwards.

## Installation


## Usage

```bash
usage: main.py [-h] [-l LOCAL_IP] [-p LOCAL_PORT] [-t TTL] -d DESTINATION [-o PORT] [-f] [-v]

options:
  -h, --help            show this help message and exit
  -l LOCAL_IP, --local_ip LOCAL_IP
  -p LOCAL_PORT, --local_port LOCAL_PORT
  -t TTL, --ttl TTL
  -d DESTINATION, --destination DESTINATION
  -o PORT, --port PORT
  -f, --flush
  -v, --verbose
```

### Example


```bash
python3 polly/main.py -d 'https://www.something.com' -o 80 -t 10
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)