# 👉😥👈 concourse-blame

This tool will continuously watch your [Concourse](https://github.com/concourse/concourse) jobs and play a sound notification depending on the current status.

⚠ Windows only, unfortunately.

## Requirements

For installation:
- Python 3 (tested with Python 3.7)
- pip
- virtualenv (optional, recommended)

For usage:
- git
- fly

## Setup

- Create virtual environment `virtualenv venv`
- Activate it: `venv/Scripts/activate.bat`
- Install dependencies by running `pip install -r requirements.txt`

## Configuration

See example.json file for configuration parameters.

## Usage

`python concourse-blame.py /path/to/config.json`

If you just want to check the voices installed on your system, run:

`python concourse-blame.py --voices`