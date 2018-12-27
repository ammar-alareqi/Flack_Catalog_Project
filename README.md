# Item Catalog
This is a simple web app that introduce categories found in a cafe. Each category has some items under it. Authenticated users can post, edit, delete their items. 

## Used Techniques 
- Python
- Flask
- SQLAlchemy
- OAuth
- HTML and CSS

## Setup
- **Vagrant** is used to run a virtual machine in with the web app will run.
- The virtual machine can be found [here](http://github.com/udacity/fullstack-nanodegree-vm)

## Installation 
- After installing the virtual machine, run the command line.
- Lunch the virtual machine using the command "vagrant up".
- Log into the virtual machine using the command "vagrant ssh".
- Navigate to "/vagrant/item_catalog/" folder.
- Run "python seeder.py".
- Run "python application.py".
- In the browser, go to: http://localhost:8000
- You can now navigate through the app.

## Notes
- To add, edit or delete any item, you have to log in using you Google acount. 
