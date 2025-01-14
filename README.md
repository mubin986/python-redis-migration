  Redis Migration Script

Redis Migration Script
======================

A Python script to migrate data between Redis instances with environment-based configuration and progress updates.

Setup
-----

1. Clone repo and navigate to the directory:

   `git clone <repo_url>`
2. Create & activate a virtual environment:

   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies using the requirements file:

   `pip install -r requirements.txt`

Requirements File
-----------------

The project dependencies are listed in the file `requirements.txt`:

    redis
    python-dotenv

Configuration
-------------

1. Copy sample env:

   cp .env.sample .env
2. Edit `.env` with your Redis credentials.

Usage
-----

Run the migration:

    python migrate.py

Script connects to source/destination Redis, migrates keys, and prints progress every 1,000 keys.

Notes
-----

* Ensure `.env` contains correct credentials.
* `.gitignore` ignores `.env` but tracks `.env.sample`.
