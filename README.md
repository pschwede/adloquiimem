# adloquiimem


An experimental bot that reposts old tweets of a particular user.

* Downloads older tweets at each run and accumulates them
* Picks a random post of them and posts it with a `@mention` of the original poster
* Replies to each thread that mentions its nick
* Cron compatible


## Installation


### On Windows

Install Linux and continue below.


### On Linux

```bash
git clone https://github.com/pschwede/adloquiimem.git
cd adloquiimem
virtualenv -p python3 .
source bin/activate
pip install -r requirements.txt
```

Now adapt `config.py` to your consumer key, consumer auth token, access key and access auth token from Twitter. Don't forget to adapt the observee and poster names in the same file.

When you are finished, you can leave the virtual environment for Python3 with:

```bash
bin/deactivate
```

After that, you can either manually run `run.sh` or add an entry in your cron tab (`crontab -e`) like this:

```bash
5 10,17 * * * /your/home/adloquiimem/run.sh
```
