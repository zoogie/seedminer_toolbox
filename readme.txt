seedminer_toolbox

- mii.py
Decrypts the Mii QR export input.bin produced from https://3ds.goombi.fr/editMii/ to output.bin.
To be used with seedminer LFCS option 3 at some point in time.

- builder.py
Adds new msed_data nodes to the lfcs(_new).dat files used for error correction in seedminer.
Not of much use for users probably.

- Ctcertifier
TADpole needs a valid ctcert from *any* 3ds to create TADs that will pass import checks on a stock 3ds.
To create this file, first run seedstarter.3dsx on a cfw system (am:net access needed) and press Y. This will dump ctcert.bin to sdmc:/seedstarter. 
To add the necessary privkey to the ctcert, run ctcertfier.firm and the privkey data will be appended to the file in that same location. 
Of course, both homebrews need to be run on the same console.

- dump_ctcert_privkey.gm9
Same function as Ctcertifier.firm. Run with Godmode9.

- graph.py
Just a little thing to visualize the msed_data nodes for my amusement.
Loads lfcs.dat and lfcs_new.dat from script directory. Needs matplotlib installed. Either py2 or py3 is fine.

- msed_data.py
Generates msed_data from a dumped movable.sed on PC.

- download.py
Just a little script for downloading msed data from Blackfall's Gitlab repo. 
Data is commited to this repo from the DIS Jenkins site.

- compat.py
Dumb little script to find compatible dsiware games based on save and executable size.
Make sure to read top of script source for extra directions.



