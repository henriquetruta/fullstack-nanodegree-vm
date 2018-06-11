# Item Catalog

## Setup

### Pre-setup

These instructions assume you're on a Vagrant machine that ran with the
Vagrantfile in the upper directory. If you're not, do:

```bash
vagrant up
vagrant ssh
```

At this moment, the PostgreSQL Database, as well as the Python environment
should already be installed.
When inside the VM, enter the proper directory with:

```bash
cd /vagrant/catalog
```

### Database
Create the Database tables and initially populate them running:

```bash
createdb catalog
python db/db_setup.py
```

### Run it!
To run the application, just do:

```bash
python application.py
```

Then, access it locally in your browser:

```
http://localhost:5000/catalog
```
