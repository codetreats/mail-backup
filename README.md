# Mail-Backup

The Mail-Backup is a docker based sync tool, which automatically syncs IMAP folders as compressed eml files.
Those files can be hosted with the [codetreats/mailarchive](https://github.com/codetreats/mailarchive).

The Mail-Backup uses scripts from [polo2ro/imapbox](https://github.com/polo2ro/imapbox)

## Usage

You simply have to adapt the config for the sync tool itself (imapbox) and the config for the enveloping docker container.
After that, you can run the `install.sh` - script.

### sync tool config (config.cfg)

The description of the sync tool can be found here:
https://github.com/polo2ro/imapbox#config-file

### container config

The container config must contain the following variables:

* CONTAINER_NAME: The name of the docker container
* CONFIG_DIR: The folder where the sync tool config (config.cfg) is located
* MAIL_FOLDER: The destination folder where all mails are synced. This folder gets never deleted by the sync tool and can be a long term backup folder.
* UNSYNCED_FOLDER: This destination contains a copy af all newly synced mails. They can be moved to a visualization tool like [codetreats/mailarchive](https://github.com/codetreats/mailarchive) 
* PIPELINE_PORT: The port where the webserver of the [pipeline](codetreats/simple-pipeline) of the sync job is running

